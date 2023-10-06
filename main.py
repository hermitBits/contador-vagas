
import cv2
import numpy as np

from gerenciador_vagas import load_vagas, width, height

vagas = load_vagas()

video = cv2.VideoCapture('video.mp4')

GREEN = (0, 255, 0)
RED = (0, 8, 255)
WHITE = (255, 255, 255)

def process_image(img):
    # conversão da imagem pra cinza
    img_cinza = cv2.cvtColor(
        src=img,
        code=cv2.COLOR_BGR2GRAY
    )
    
    # binariza imagem preto/branco
    img_threshold = cv2.adaptiveThreshold(
        src=img_cinza,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY_INV,
        blockSize=25,
        C=16
    )
    
    # suavizar pixels
    img_blur = cv2.medianBlur(
        src=img_threshold,
        ksize=5
    )
    
    # dilatar os pixels
    kernel = np.ones((3, 3), np.int8)
    img_dilate = cv2.dilate(
        src=img_blur,
        kernel=kernel
    )
    
    return img_dilate

while True:
    ret, img = video.read()
    
    # testar se video já terminou
    if not ret:
        break
    
    # morfologizar imagem
    img_process = process_image(img)
    
    for vaga in vagas:
        # isolar as vagas
        recorte = img_process[vaga.y:vaga.y+height, vaga.x:vaga.x+width]
        
        # contar a quantidade de pixels brancos nelas
        qtd_pixels_brancos = cv2.countNonZero(recorte)
        
        # imprimir no canto inferior esquerdo a quantidade de pixels contados
        cv2.putText(
            img=img, 
            text=f'{qtd_pixels_brancos}',
            org=(vaga.x,vaga.y+height-10),
            fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
            fontScale=0.5,
            color=WHITE,
            thickness=1
        )
        
        # desenhar retangulo nas vagas, as vaga que contém carro retangulo
        # vermelho e sem carro verde.
        color = GREEN
        if qtd_pixels_brancos > 3000:
            color = RED
            
        cv2.rectangle(img, vaga.pt1, vaga.pt2, color, thickness=3)
    
    # exibe o video    
    cv2.imshow('video', img)
    
    # testa se video acabou e se a tecla que Q foi precissionada para sair
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()