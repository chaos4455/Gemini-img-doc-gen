# -*- coding: utf-8 -*-

import sys
import os
import math
import time
import hashlib # Para calcular hash
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass # Para estrutura de dados organizada

try:
    from PIL import Image, ImageFile
    ImageFile.LOAD_TRUNCATED_IMAGES = True
except ImportError:
    print("Erro: Biblioteca Pillow não encontrada. Instale com 'pip install Pillow'")
    sys.exit(1)

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                             QMainWindow, QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

# --- Constantes ---
RESIZE_FACTOR = 0.50
RESAMPLING_FILTER = Image.Resampling.LANCZOS if hasattr(Image, 'Resampling') else Image.LANCZOS

# --- Estrutura de Dados para Informações da Imagem ---
@dataclass
class ProcessedImageInfo:
    original_path: str
    creation_time: float
    content_hash: str
    resized_image: Image.Image # A imagem PIL já redimensionada

# --- Worker Thread ---
class CollageWorker(QThread):
    progress_update = pyqtSignal(int, str)
    collage_finished = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, image_paths, save_dir):
        super().__init__()
        self.image_paths = image_paths
        self.save_dir = save_dir
        # Lista para armazenar as informações completas de cada imagem processada
        self.processed_image_info_list: list[ProcessedImageInfo] = []
        # Lista final apenas com as imagens PIL a serem usadas na colagem
        self.pil_images_for_collage: list[Image.Image] = []
        self.is_cancelled = False
        self.num_workers = min(len(image_paths), (os.cpu_count() or 1) * 2)

    def run(self):
        start_time = time.time()
        try:
            # --- Etapa 1: Carregamento, Hash, Redimensionamento Paralelo ---
            self._process_images_parallel()
            if self.is_cancelled or not self.processed_image_info_list: return

            # --- Etapa 2: Filtragem de Duplicatas ---
            initial_count = len(self.processed_image_info_list)
            self.progress_update.emit(55, f"Filtrando duplicatas de {initial_count} imagens...")
            self._filter_duplicates()
            final_count = len(self.pil_images_for_collage)
            removed_count = initial_count - final_count
            filter_msg = f"Filtragem concluída. {final_count} imagens únicas."
            if removed_count > 0:
                filter_msg += f" ({removed_count} duplicatas removidas)."
            print(filter_msg) # Log no console
            self.progress_update.emit(60, filter_msg) # Atualiza GUI

            if self.is_cancelled or not self.pil_images_for_collage:
                 if not self.is_cancelled: # Só emite erro se não foi cancelado
                    self.error_occurred.emit("Nenhuma imagem restante após filtrar duplicatas.")
                 return

            # --- Etapa 3: Calcular Grade e Dimensões (usa imagens filtradas) ---
            self.progress_update.emit(65, "Calculando layout da grade...")
            cols, rows, cell_width, cell_height = self._calculate_grid_dimensions()
            if self.is_cancelled: return

            # --- Etapa 4: Criar Imagem da Colagem (usa imagens filtradas) ---
            self.progress_update.emit(70, f"Criando tela da colagem ({cols}x{rows})...")
            collage_image = self._create_collage_image(cols, rows, cell_width, cell_height)
            if self.is_cancelled or collage_image is None: return

            # Libera memória das infos e imagens processadas
            del self.processed_image_info_list
            self.processed_image_info_list = []
            del self.pil_images_for_collage
            self.pil_images_for_collage = []

            # --- Etapa 5: Salvar Imagem Final ---
            self.progress_update.emit(95, "Salvando colagem no disco...")
            final_path = self._save_collage_image(collage_image)
            if self.is_cancelled: return

            # --- Conclusão ---
            end_time = time.time()
            duration = end_time - start_time
            self.progress_update.emit(100, f"Colagem salva! ({duration:.2f}s)")
            self.collage_finished.emit(final_path)

        except Exception as e:
            print("Erro detalhado no worker:")
            traceback.print_exc()
            self.error_occurred.emit(f"Erro inesperado: {e}")
        finally:
            # Garante limpeza final
            self.processed_image_info_list = []
            self.pil_images_for_collage = []

    def _process_images_parallel(self):
        """Carrega, obtém hash/ctime, redimensiona em paralelo."""
        num_images = len(self.image_paths)
        self.progress_update.emit(0, f"Iniciando processamento de {num_images} imagens...")
        processed_count = 0
        process_errors = 0

        with ThreadPoolExecutor(max_workers=self.num_workers, thread_name_prefix='ImgProc') as executor:
            # Submete a tarefa que retorna a estrutura ProcessedImageInfo
            future_to_path = {executor.submit(self.process_single_image, path): path for path in self.image_paths}

            for future in as_completed(future_to_path):
                if self.is_cancelled:
                    for f in future_to_path: f.cancel()
                    # Não emitir erro aqui, run() tratará
                    return

                path = future_to_path[future]
                try:
                    # Espera o resultado (ProcessedImageInfo ou None)
                    image_info = future.result()
                    if isinstance(image_info, ProcessedImageInfo):
                        self.processed_image_info_list.append(image_info)
                    elif image_info is None: # Erro ocorreu dentro de process_single_image
                        process_errors += 1
                except Exception as exc:
                    print(f"Erro ao obter resultado para {os.path.basename(path)}: {exc}")
                    process_errors += 1
                finally:
                    processed_count += 1
                    # Processamento agora vai até ~55%
                    progress = int((processed_count / num_images) * 55)
                    if processed_count % 5 == 0 or processed_count == num_images:
                        msg = f"Processando: {processed_count}/{num_images}"
                        if process_errors > 0:
                            msg += f" ({process_errors} erros)"
                        self.progress_update.emit(progress, msg)

        # Não emite erro aqui se algumas imagens falharam, a menos que NENHUMA tenha sido processada
        if not self.processed_image_info_list and process_errors > 0:
            self.error_occurred.emit(f"Nenhuma imagem pôde ser processada ({process_errors} erros).")
        elif process_errors > 0:
             print(f"Aviso: Falha ao processar {process_errors} de {num_images} imagens.")


    def process_single_image(self, image_path) -> ProcessedImageInfo | None:
        """Carrega, obtém hash/ctime, converte modo e redimensiona UMA imagem."""
        try:
            # Obter tempo de criação primeiro (menos propenso a falhar que o carregamento)
            try:
                 creation_time = os.path.getctime(image_path)
            except OSError as e:
                 print(f"Erro ao obter ctime para '{os.path.basename(image_path)}': {e}")
                 return None # Não podemos comparar sem ctime

            # Carregar imagem
            img = Image.open(image_path)
            img.load()

            # Calcular hash do conteúdo ANTES de converter ou redimensionar
            # Usar tobytes() é geralmente mais rápido que reler o arquivo
            try:
                image_bytes = img.tobytes()
                content_hash = hashlib.sha256(image_bytes).hexdigest()
                del image_bytes # Liberar memória
            except Exception as e:
                print(f"Erro ao calcular hash para '{os.path.basename(image_path)}': {e}")
                return None # Não podemos comparar sem hash

            # Converter modos (após hash)
            original_mode = img.mode
            if original_mode == 'P': img = img.convert('RGBA')
            elif original_mode == 'L': img = img.convert('RGB')
            elif original_mode not in ['RGB', 'RGBA']: img = img.convert('RGB')

            # Redimensionar (após hash e conversão)
            w_orig, h_orig = img.size
            w_new = max(1, int(w_orig * RESIZE_FACTOR))
            h_new = max(1, int(h_orig * RESIZE_FACTOR))
            resized_img = img.resize((w_new, h_new), RESAMPLING_FILTER)

            # Retornar a estrutura completa
            return ProcessedImageInfo(
                original_path=image_path,
                creation_time=creation_time,
                content_hash=content_hash,
                resized_image=resized_img
            )

        except FileNotFoundError:
             print(f"Erro: Arquivo não encontrado: {os.path.basename(image_path)}")
             return None
        except Exception as e:
            print(f"Erro ao processar '{os.path.basename(image_path)}': {e}")
            return None

    def _filter_duplicates(self):
        """Filtra a lista processed_image_info_list, mantendo os mais antigos."""
        if not self.processed_image_info_list:
            self.pil_images_for_collage = []
            return

        best_by_hash: dict[str, tuple[float, int]] = {} # hash -> (ctime, index)
        best_by_filename: dict[str, tuple[float, int]] = {} # basename -> (ctime, index)

        for index, info in enumerate(self.processed_image_info_list):
            current_hash = info.content_hash
            # Normalizar nome do arquivo (lowercase, ignorar extensão?) - Vamos usar basename por enquanto
            current_basename = os.path.basename(info.original_path)
            current_ctime = info.creation_time

            # Atualizar melhor por hash
            if current_hash not in best_by_hash or current_ctime < best_by_hash[current_hash][0]:
                best_by_hash[current_hash] = (current_ctime, index)

            # Atualizar melhor por nome de arquivo
            if current_basename not in best_by_filename or current_ctime < best_by_filename[current_basename][0]:
                best_by_filename[current_basename] = (current_ctime, index)

        # Coletar os índices únicos dos itens a serem mantidos
        final_indices_to_keep = set()
        for _, index in best_by_hash.values():
            final_indices_to_keep.add(index)
        for _, index in best_by_filename.values():
            final_indices_to_keep.add(index)

        # Criar a lista final de imagens PIL para a colagem
        # Mantém a ordem original de arraste/solte o máximo possível
        self.pil_images_for_collage = [
            self.processed_image_info_list[i].resized_image
            for i in sorted(list(final_indices_to_keep)) # Ordena por índice original
        ]


    def _calculate_grid_dimensions(self):
        """Calcula dimensões da grade baseado nas imagens JÁ FILTRADAS."""
        num_images = len(self.pil_images_for_collage) # Usa a lista filtrada
        if num_images == 0:
            # Este erro não deveria acontecer se a verificação em run() estiver correta
            raise ValueError("Nenhuma imagem final para calcular dimensões.")

        cols = math.ceil(math.sqrt(num_images))
        rows = math.ceil(num_images / cols)

        max_w, max_h = 0, 0
        for img in self.pil_images_for_collage: # Usa a lista filtrada
            w, h = img.size
            max_w = max(w, max_w)
            max_h = max(h, max_h)

        if max_w == 0 or max_h == 0:
             raise ValueError("Dimensões de imagem filtrada inválidas.")

        return cols, rows, max_w, max_h

    def _create_collage_image(self, cols, rows, cell_width, cell_height):
        """Cria a imagem final colando as imagens FILTRADAS."""
        collage_width = cols * cell_width
        collage_height = rows * cell_height
        try:
            # Verificar se as dimensões não são excessivas antes de criar
            # Limite arbitrário (ex: 65500 pixels, comum em algumas libs)
            max_dimension = 65500
            if collage_width > max_dimension or collage_height > max_dimension:
                 self.error_occurred.emit(f"Dimensões da colagem ({collage_width}x{collage_height}) excedem o limite. Muitas imagens ou imagens muito grandes.")
                 return None
            collage_image = Image.new('RGB', (collage_width, collage_height), (0, 0, 0))
        except ValueError as e:
             self.error_occurred.emit(f"Erro ao criar tela ({collage_width}x{collage_height}): {e}.")
             return None

        current_image_index = 0
        paste_total = len(self.pil_images_for_collage) # Usa a lista filtrada

        for r in range(rows):
            for c in range(cols):
                if self.is_cancelled: return None
                if current_image_index < paste_total:
                    img_to_paste = self.pil_images_for_collage[current_image_index] # Usa a lista filtrada
                    img_w, img_h = img_to_paste.size
                    cell_x = c * cell_width
                    cell_y = r * cell_height
                    paste_x = cell_x + (cell_width - img_w) // 2
                    paste_y = cell_y + (cell_height - img_h) // 2

                    try:
                        if img_to_paste.mode == 'RGBA':
                            mask = img_to_paste.split()[-1]
                            collage_image.paste(img_to_paste, (paste_x, paste_y), mask=mask)
                        else:
                            collage_image.paste(img_to_paste, (paste_x, paste_y))
                    except IndexError:
                         print(f"Aviso: Problema ao obter máscara alfa para imagem {current_image_index}, colando sem transparência.")
                         collage_image.paste(img_to_paste.convert('RGB'), (paste_x, paste_y))
                    except Exception as e:
                         print(f"Erro ao colar imagem {current_image_index}: {e}")
                         # Decide: Parar ou continuar? Vamos continuar.

                    current_image_index += 1
                    # Ajuste percentual da colagem: 70-95%
                    progress = 70 + int((current_image_index / paste_total) * 25)
                    if current_image_index % 10 == 0 or current_image_index == paste_total:
                         self.progress_update.emit(progress, f"Montando colagem: {current_image_index}/{paste_total}")
                else:
                    break
            if current_image_index >= paste_total:
                break

        return collage_image

    # _save_collage_image, generateUniqueName, cancel permanecem iguais

    def _save_collage_image(self, collage_image):
        """Salva a imagem da colagem no disco."""
        if collage_image is None:
             raise ValueError("Imagem da colagem não foi criada ou ocorreu erro.")

        unique_name = self.generateUniqueName()
        # Nome reflete redimensionamento e filtragem
        filename = os.path.join(self.save_dir, f'colagem_filtrada_{unique_name}.png')

        if not os.path.exists(self.save_dir):
            try: os.makedirs(self.save_dir)
            except OSError as e: raise OSError(f"Erro fatal ao criar diretório '{self.save_dir}' antes de salvar: {e}") from e

        try:
            collage_image.save(filename, "PNG", quality=95)
            return filename
        except Exception as e:
             raise IOError(f"Erro ao salvar a imagem final em {filename}: {e}") from e

    def generateUniqueName(self):
        timestamp = int(time.time() * 1000)
        random_part = hashlib.md5(os.urandom(8)).hexdigest()[:8]
        return f"{timestamp}_{random_part}"

    def cancel(self):
        print("Sinal de cancelamento recebido pelo worker.")
        self.is_cancelled = True


# --- Main GUI Widget (pequenas alterações em textos e save_path) ---
class ImageCollage(QWidget):
    def __init__(self):
        super().__init__()
        self.worker_thread = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Criador de Colagens (Redim. + Anti-Duplicata)')
        self.setMinimumSize(500, 350)

        self.layout = QVBoxLayout()
        self.label = QLabel(f'Arraste imagens aqui.\n({int(RESIZE_FACTOR*100)}% do original, duplicatas removidas pelo mais antigo)')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.base_style = 'border: 2px dashed blue; padding: 20px; font-size: 14px;'
        self.label.setStyleSheet(self.base_style)

        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setVisible(False)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.progressBar)
        self.setLayout(self.layout)

        self.setAcceptDrops(True)
        self.save_path = r'C:\colagens_filtradas' # Novo caminho

    # dragEnterEvent, dragLeaveEvent, dropEvent, startProcessing, slots (updateProgress, etc.)
    # e métodos auxiliares (showError, resetLabel, etc.) permanecem praticamente os mesmos
    # Apenas o texto inicial em resetLabel precisa ser atualizado.

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() and not (self.worker_thread and self.worker_thread.isRunning()):
            event.acceptProposedAction()
            self.label.setStyleSheet('border: 2px dashed red; padding: 20px; font-size: 14px;')
            self.label.setText('Solte as imagens para iniciar...')
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        if not (self.worker_thread and self.worker_thread.isRunning()):
             self.resetLabelStyle()

    def dropEvent(self, event: QDropEvent):
        if self.worker_thread and self.worker_thread.isRunning():
            QMessageBox.warning(self, "Ocupado", "Aguarde o processamento atual terminar.")
            return

        urls = event.mimeData().urls()
        imagePaths = []
        valid_extensions = ('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif', '.tiff', '.tif')
        for url in urls:
            file_path = url.toLocalFile()
            if os.path.isfile(file_path) and file_path.lower().endswith(valid_extensions):
                imagePaths.append(file_path)

        if not imagePaths:
            self.showError("Nenhuma imagem válida encontrada.")
            self.resetLabelStyle()
            return

        try:
            if not os.path.exists(self.save_path): os.makedirs(self.save_path)
        except OSError as e:
            self.showError(f"Erro CRÍTICO ao criar diretório:\n{self.save_path}\n{e}\nVerifique permissões.", critical=True)
            return

        self.startProcessing(imagePaths)

    def startProcessing(self, imagePaths):
        self.label.setText("Iniciando...")
        self.label.setStyleSheet('border: 2px solid orange; padding: 20px; font-size: 14px;')
        self.progressBar.setValue(0)
        self.progressBar.setVisible(True)
        self.setAcceptDrops(False)
        QApplication.processEvents()

        self.worker_thread = CollageWorker(imagePaths, self.save_path)
        self.worker_thread.progress_update.connect(self.updateProgress)
        self.worker_thread.collage_finished.connect(self.onProcessingFinished)
        self.worker_thread.error_occurred.connect(self.onProcessingError)
        self.worker_thread.finished.connect(self.onWorkerThreadFinished)
        self.worker_thread.start()

    def updateProgress(self, percentage, message):
        self.progressBar.setValue(percentage)
        self.progressBar.setFormat(f"%p% - {message}")

    def onProcessingFinished(self, saved_path):
        # Tenta extrair a mensagem final da barra de progresso (inclui tempo e contagem)
        progress_text_parts = self.progressBar.format().split("-")
        status_message = progress_text_parts[-1].strip() if len(progress_text_parts) > 1 else "Concluído!"
        final_message = f'Sucesso! {status_message}\nSalvo em:\n{saved_path}'

        self.label.setStyleSheet('border: 2px solid green; padding: 20px; font-size: 14px;')
        self.label.setText(final_message)
        self.progressBar.setVisible(False)
        self.progressBar.setFormat("%p%")
        self.setAcceptDrops(True)
        QTimer.singleShot(10000, self.resetLabel)

    def onProcessingError(self, error_message):
        self.showError(f"Erro durante o processamento:\n{error_message}", critical=True)
        self.progressBar.setVisible(False)
        self.progressBar.setFormat("%p%")
        self.setAcceptDrops(True)

    def onWorkerThreadFinished(self):
        print("Worker thread finalizado.")
        self.worker_thread = None
        self.setAcceptDrops(True) # Garante que drops estejam habilitados

    def showError(self, message, critical=False):
        print(f"GUI Error Display: {message}")
        if critical:
            QMessageBox.critical(self, "Erro Crítico", message)
            self.resetLabel() # Resetar após erro crítico
        else:
            # Erros não críticos na label
            self.label.setStyleSheet('border: 2px solid red; padding: 20px; font-size: 14px; color: red;')
            self.label.setText(message)
            QTimer.singleShot(6000, self.resetLabel) # Resetar após um tempo

    def resetLabel(self):
        if not (self.worker_thread and self.worker_thread.isRunning()):
            # Atualiza texto inicial
            self.label.setText(f'Arraste imagens aqui.\n({int(RESIZE_FACTOR*100)}% do original, duplicatas removidas pelo mais antigo)')
            self.resetLabelStyle()
            self.progressBar.setVisible(False)

    def resetLabelStyle(self):
         self.label.setStyleSheet(self.base_style + "color: black;")

    def closeEvent(self, event):
        if self.worker_thread and self.worker_thread.isRunning():
            reply = QMessageBox.question(self, 'Processamento em Andamento',
                                           "Deseja cancelar o processo atual e sair?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                print("Usuário solicitou cancelamento ao fechar.")
                self.worker_thread.cancel()
                self.worker_thread.wait(500)
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


# --- Main Application Setup ---
class MainWindow(QMainWindow):
    # ... (igual à versão anterior) ...
    def __init__(self):
        super().__init__()
        self.collageWidget = ImageCollage()
        self.setCentralWidget(self.collageWidget)
        self.setWindowTitle(self.collageWidget.windowTitle())
        self.resize(650, 450)

    def closeEvent(self, event):
        self.collageWidget.closeEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
