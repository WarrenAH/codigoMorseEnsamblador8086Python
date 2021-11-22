import os
import time
import dropbox

token = "sl.A8uzGFlswydY4lzYZTCMwOtUQLD7j5JV6EOQtlVP32UvSQqC7epwsZsAybCPiYwH3fNF_XvdR4s4VODkjx_WbbD9tTrwfRaw2z3OjdYL0Bkkl9HSUbFmaFhk4rb2pJFZyqugqnk"
dbx = dropbox.Dropbox(token)

def codigoMorseALetras(archivo):
    traduccionesCodigoMorse = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..',
             'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-',
             'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
             'Z': '--..', ' ': '/', '': ' '}

    traduccionesCodigoMorseLista = {v: k for k, v in traduccionesCodigoMorse.items()}
    print(' '.join([''.join([traduccionesCodigoMorseLista[c] for c in word.split(' ')]) for word in archivo.split('  ')]))

    return ' '.join([''.join([traduccionesCodigoMorseLista[c] for c in word.split(' ')]) for word in archivo.split('  ')])

def revisarDirectorios():
    if not os.path.isdir('C:/emu8086/vdrive/c'):
        os.mkdir('C:/emu8086/vdrive/c')

    if not os.path.isdir('C:/emu8086/vdrive/c/traduccionMensaje'):
        os.mkdir('C:/emu8086/vdrive/c/traduccionMensaje')

    carpetaBorrar = 'C:/emu8086/vdrive/c/traduccionMensaje'
    for carpeta in os.listdir(carpetaBorrar):
        ubicacionCarpeta = os.path.join(carpetaBorrar, carpeta)
        try:
            if os.path.isfile(ubicacionCarpeta):
                os.unlink(ubicacionCarpeta)
        except Exception as e:
            print(e)

def realizarTraduccion():
    if os.path.exists('C:/emu8086/vdrive/c/programaTerminado.txt'):
        os.remove('C:/emu8086/vdrive/c/programaTerminado.txt')
        print("")
        print("El archivo se encontro, se procedera a revisar.")
        with open('C:/emu8086/vdrive/c/codigoMorse.txt', 'r') as archivo:
            textoCodigoMorse = archivo.read().rstrip('\n')
            print("")
            print(textoCodigoMorse)
            print("")

            archivoNuevo = open("C:/emu8086/vdrive/c/traduccionMensaje/nuevoMensajeRecibido.txt", "w")
            archivoNuevo.write(str((codigoMorseALetras(textoCodigoMorse))))
            archivoNuevo.close()

            print("")
            print("El mensaje fue correctamente traducido, ahora, se subira a Dropbox.")
        return

    else:
        print("")
        print("El archivo no existe, se volvera a llamar la funcion.")
        time.sleep(15)
        realizarTraduccion()

def descargarMostrarRespuesta():
    print("Mensaje entrante:")

    with open("mensajeRecibidoReceptor.txt", "wb") as archivo:
        metadata, descargarRespuesta = dbx.files_download(path="/bandejaMensajeReceptor/nuevoMensajeRecibido.txt")
        archivo.write(descargarRespuesta.content)

    with open('mensajeRecibidoReceptor.txt', 'r') as archivo:
        textoRespuesta = archivo.read().rstrip('\n')
        print("")
        print(textoRespuesta)
        print("")

    os.remove("mensajeRecibidoReceptor.txt")

def subirADropbox():
    usuario = dbx.users_get_current_account()
    print(usuario)

    archivoPC = "C:/emu8086/vdrive/c/traduccionMensaje/nuevoMensajeRecibido.txt"
    archivoSubir = '/bandejaMensajeEmisor/nuevoMensajeRecibido.txt'

    dbx.files_upload(open(archivoPC, 'rb').read(), archivoSubir,  mode=dropbox.files.WriteMode("overwrite"))

    print("")
    print("El mensaje fue subido a Dropbox.")

def desicion():
    escoger = input("¿Desea responder al mensaje? Presione 1, en caso contrario presione 2 para salir.\n")
    escoger=int(escoger)

    if escoger==1:
        revisarDirectorios()
        realizarTraduccion()
        subirADropbox()

    if escoger==2:
        exit()

    if escoger !=1 and escoger!=2:
        print("")
        print("Solo son validos los numeros 1 y 2.")
        print("")
        desicion()

descargarMostrarRespuesta()
desicion()


