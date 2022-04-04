#------------------------------ Importamos las librerias ------------------------------
import cv2
import mediapipe as mp
import serial

#----------------------------- Puerto Serial Configuracion ----------------------------
com = serial.Serial("COM3", 9600, write_timeout= 10)
d = 'd'
i = 'i'
p = 'p'

#------------------------------ Declaramos el detector --------------------------------
detector = mp.solutions.face_detection
dibujo = mp.solutions.drawing_utils

#------------------------------ Realizamos VideoCaptura --------------------------------
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#-------------------------------Empezamos el while True --------------------------------
with detector.FaceDetection(min_detection_confidence=0.75) as rostros:
    while True:
        ret, frame = cap.read()

        #Aplicamos espejo a los frames
        frame = cv2.flip(frame,1)

        #Correccion de color
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #Detectamos los rostros
        resultado = rostros.process(rgb)


        #Si hay rostros entramos al if
        if resultado.detections is not None:
            for rostro in resultado.detections:
                dibujo.draw_detection(frame, rostro, dibujo.DrawingSpec(color=(0,255,0),))

                for id, puntos in enumerate(resultado.detections):
                    #Mostramos toda la informacion
                    #print("Puntos: ", resultado.detections)

                    #Extraemos el ancho y el alto del frame
                    al, an, c = frame.shape

                    #Extraemos el medio de la pantalla
                    centro = int(an / 2)

                    #Extraemos las coordenadas X e Y min
                    x = puntos.location_data.relative_bounding_box.xmin
                    y = puntos.location_data.relative_bounding_box.ymin

                    #Extraemos el ancho y el alto
                    ancho = puntos.location_data.relative_bounding_box.width
                    alto = puntos.location_data.relative_bounding_box.height

                    #Pasamos X e Y a coordenadas en pixeles
                    x, y = int(x * an), int(y * al)
                    print("X, Y: ", x, y)

                    #Pasamos el ancho y el alto a pixeles
                    x1, y1 = int(ancho * an), int(alto * al)

                    #Extraemos el punto central
                    cx = (x + (x + x1)) // 2
                    cy = (y + (y + y1)) // 2
                    #print("Centro: ", cx, cy)

                    #Mostrar un punto en el centro
                    cv2.circle(frame, (cx, cy), 3, (0, 0, 255), cv2.FILLED)
                    cv2.line(frame, (cx, 0), (cx, 480), (0, 0, 255), 2)

                    #Condiciones para mover el servo
                    if cx < centro - 50:
                        #Movemos hacia la izquierda
                        print("Izquierda")
                        com.write(i.encode('ascii'))
                    elif cx > centro + 50:
                        #Movemos hacia la derecha
                        print("Derecha")
                        com.write(d.encode('ascii'))
                    elif cx == centro:
                        #Paramos el servo
                        print("Parar")
                        com.write(p.encode('ascii'))


        cv2.imshow("Camara", frame)
        t = cv2.waitKey(1)
        if t == 27:
            break
cap.release()
cv2.destroyAllWindows()