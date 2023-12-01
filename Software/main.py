import machine
from machine import Pin,I2C,PWM,ADC
import ssd1306
import time
# variables globales
switch=0
contadorBtn=0
contadorSec=0
#tiemnpo para procesar
MinPan=30
SecPan=00
MinMogolla=45
# Inicializar la lista de datos de temperatura
datos_temperatura = []
SecMogolla=00
MinAli=0
SecAli=0
MosGraf=0
#pantalla
i2c=I2C(0,scl=Pin(22),sda=Pin(21))
oled=ssd1306.SSD1306_I2C(128,64,i2c)
oled_width = 128
oled_height = 64
fila_libre = 10 
#funciones
#temporizador
def temporizador(segundos):
    for s in range(segundos,0,-1):
        print("comence")
        return s
    
#borrar
def borrar_pantalla():
    oled.fill(0)
    oled.show()

# Configuración del sensor LM35
LM35_pin = machine.Pin(33)
adc = machine.ADC(LM35_pin)
#mostrar mensaje
def MostrarUpdate():
    borrar_pantalla()
    oled.text("Tiempo  ",2,20)
    oled.text("Iniciado: ",16,40)
    oled.show()
    time.sleep(1)
    borrar_pantalla()
#mostrar pantalla
def mostrarGrafica():
    oled.text("SELECCIONE MODO",0,0)
    oled.text("(1)Grafica",2,18)
    oled.text("(2)Tiempo",2,28)
    oled.text("(3)Alimento",2,38)
    oled.text("(4)Apagar",2,48)
    oled.text("T",2,58)
    oled.text(str (SecAli),16,58)
    oled.show()
#mostrar grafica
def MostrarGraficaPrim():
    global MosGraf,contadorBtn, contadorSec,MinAli,SecAli
    print("Llegue a la uncion")
    print("valor: ",MosGraf)
    while MosGraf==1:
        print("Muestro tu grafica")
        if contadorBtn == 0:
            break
        if SecAli>0:
            MinAli-=1
        # Obtener datos de temperatura del sensor LM35
        temperatura = (adc.read() / 4095) * 60 # Convertir lectura ADC a temperatura en grados Celsius
        datos_temperatura.append((len(datos_temperatura), temperatura))
        if len(datos_temperatura) > 10:
            datos_temperatura.pop(0)  # Limitar la cantidad de puntos para mostrar en la pantalla

        # Encontrar el máximo valor de temperatura
        max_valor = max(datos_temperatura, key=lambda x: x[1])[1]
        escala_y = (oled_height - fila_libre) / (max_valor+1)

        # Limpiar la pantalla
        oled.fill(0)

        # Dibujar líneas entre los puntos
        for i in range(len(datos_temperatura) - 1):
            x1 = int((i / (len(datos_temperatura) - 1)) * oled_width)
            y1 = int(oled_height - fila_libre - (datos_temperatura[i][1] * escala_y))
            x2 = int(((i + 1) / (len(datos_temperatura) - 1)) * oled_width)
            y2 = int(oled_height - fila_libre - (datos_temperatura[i + 1][1] * escala_y))
            oled.line(x1, y1, x2, y2, 1)

        # Dibujar etiquetas de ejes
        oled.text('Tiempo: T:{}'.format(MinAli, SecAli), 0, oled_height - fila_libre, 1)
        oled.text('T actual: {:.2f}'.format(datos_temperatura[-1][1]), 0, oled_height - 2 * fila_libre, 1)

        # Mostrar la pantalla
        oled.show()
        
        time.sleep(1)  # Esperar un segundo antes de la siguiente actualización


#mostrar tiempo
def MostrarTiempoPrim():
    #borrar_pantalla()
    oled.text("Segundo Modo",0,0)
    oled.fill_rect(5, 24, 16, 7, 0) # draw a solid rectangle starting at 10,10 length 117 height 53, colour=1
    oled.text(str(MinAli),5,24)
    oled.text("__",5,26)
    oled.text("|",20,24)
    oled.text("Min",0,37)
    oled.fill_rect(30, 24, 16, 7, 0) # draw a solid rectangle starting at 10,10 length 117 height 53, colour=1
    oled.text(str(SecAli),36,24)
    oled.text(str(SecAli),28,24)
    oled.text("__",27,26)
    oled.text("Seg",27,37)
    oled.text("(1)Up",55,16)
    oled.text("(2)Down",55,28)
    oled.text("(3)exit",55,40)
    oled.text("(4)Start",55,52)
    oled.show()
#mostrar opciones
def mostrarTerOpcion():
    oled.text("SELECCIONE ALIMENTO",0,0)
    oled.text("(1)Pan",2,20)
    oled.text("(2)Mogolla",2,30)
    oled.text("(3)Cancelar",2,40)
    oled.show()

#3
def rapido():
    #sonido(1, 0.5, 512)
    Zumba.freq(1)
    Zumba.duty(512)
    time.sleep(.5)
    Zumba.duty(0)
def sonido(freq, sleep, duty):
    print("reproduje")
    Zumba.freq(freq)
    Zumba.duty(duty)
    time.sleep(sleep)
    Zumba.duty(0)
#botones
def AtiendeInterrupcion (pin):
    print ("llegue")
    global contadorBtn, switch
    global MinAli
    if contadorBtn == 0:
            # Aquí puedes agregar la lógica para volver al menú principal
            # Por ejemplo, establecer MosGraf en 0 para salir del bucle de MostrarGraficaPrim
            print("llegue2")
            MosGraf= 0
    if contadorBtn==4:
        contadorBtn=0;
    #tercer boton cancelaer
    if pin==Pin(4):
        rapido()
        if contadorBtn==0:
            contadorBtn=3
            borrar_pantalla()
        else:
            borrar_pantalla()
            contadorBtn=0
    elif pin==Pin(16):
#segundo mBOTON
        rapido()
        if contadorBtn==0:
            contadorBtn=2
            
            borrar_pantalla()
            #MostrarTiempoPrim()
        elif contadorBtn==2:
            MinAli-=1
            if MinAli<0:
                MinAli=0
        elif contadorBtn==3:
            #selecciona alimento modificando la variable
            SecAli=SecMogolla
            MinAli=MinMogolla
            contadorBtn=0
            borrar_pantalla()
        print("Interrumpe: 2")
    #primer btn
    elif pin==Pin(17):
        rapido()
        if contadorBtn==0:
            contadorBtn=1
            borrar_pantalla()
        elif contadorBtn==2:
            MinAli=MinAli+1
    elif pin==Pin(5):#boton 4
        rapido()
        if contadorBtn==0:
            if switch>1:
                switch=0
                
            if switch==0:
                rapido()
                oled.poweroff()     # power off the display, pixels persist in memory
                switch+=1
            elif switch==1:
                switch+=1
                rapido()
                oled.poweron()      # power on the display, pixels redrawn
            print("switch",switch)
        elif contadorBtn==2:
            contadorBtn=0
            print("tiempo iniciado")
            MostrarUpdate()
            contadorSec=1

        #botones
    #print("Interrumpe: ",pin)
    print("	contador: ",contadorBtn)
p4  =  Pin( 5 ,  Pin.IN ,  Pin.PULL_UP )
p4.irq (trigger=Pin.IRQ_FALLING, handler=AtiendeInterrupcion)
p3  =  Pin( 4 ,  Pin.IN ,  Pin.PULL_UP )
p3.irq (trigger=Pin.IRQ_FALLING, handler=AtiendeInterrupcion)

p2  =  Pin( 16 ,  Pin.IN ,  Pin.PULL_UP )
p2.irq (trigger=Pin.IRQ_FALLING, handler=AtiendeInterrupcion)

p1  =  Pin( 17 ,  Pin.IN ,  Pin.PULL_UP )
p1.irq (trigger=Pin.IRQ_FALLING, handler=AtiendeInterrupcion)
#zumbador
Zumba=PWM(Pin(2),freq=440,duty=0)#duty puede ir de 0 a 1024
SecAli=MinAli*3600
while True:
    if contadorSec==1:
        print(SecAli)
        SecAli-=1
    if contadorBtn==0:
        print("estoy en el menu")
        mostrarGrafica()
    elif contadorBtn==1:
        MosGraf=1
        MostrarGraficaPrim()
    elif contadorBtn==2:
        MostrarTiempoPrim()
    elif contadorBtn==3:
        mostrarTerOpcion()
    #for i in range(0,5):
        #print("xd",i)
        #oled.text(str(i),10,10)
        #oled.show()
        #time.sleep(2)
        #oled.fill(0)
        
    #oled.text('hi',10,10)
    #oled.show()