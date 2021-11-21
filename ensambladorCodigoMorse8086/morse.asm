.model tiny
.data
      puntoCodigoMorse db ".","$"      
      lineaCodigoMorse db "-","$"
      espacioCodigoMorse db " ","$"
      espacioNuevaPalabraCodigoMorse db "/","$"
      verEspacioCodigoMorse db "+","$"
       
      crearArchivo db "c:\codigoMorse.txt",00 
             
      finalizarConArchivo db "c:\programaTerminado.txt",00   
      
      handle dw ? 
      
      contador dw 0h 
      
      revisarEspacioPrograma equ 32
      revisarZPrograma equ 122
      revisarEnterPrograma equ 13
      
.code
	.startup
	 
    crearElArchivo crearArchivo
    
    imprimirEnPantalla macro mensaje
        lea dx,mensaje 
        mov ah,09H
        int 21H
        
        call escribirTxt 
	endm
	
	escribirEnArchivo macro mensaje
        mov ah, 42h
        mov bx, handle
        mov al, 0
        mov cx, 0
        mov dx, contador
        int 21h
    
        mov ah, 40h
        mov bx, handle
        mov dx, offset mensaje
        mov cx, 1
        int 21h
    
        add contador, 1h
    
        jmp revisarMouse 
	endm
	
	crearElArchivo macro archivo
	    mov ah, 3ch
	    mov cx, 0
	    mov dx, offset archivo
	    mov ah, 3ch
	    int 21h  
	endm
	
	revisarMouse:               
    mov ax,0x3
    int 0x33
    test bl,1
    jnz clickIzquierdoPresionado
    test bl,2
    jnz clickDerechoPresionado
      
    mov ah, 01h
    int 16h
    cmp al, revisarEnterPrograma 
    je finalizarPrograma
    
    mov ah, 1h   
    int 16h
    jz revisarM     
    mov ah, 0h   
    int 16h
    cmp al, revisarEspacioPrograma  
    je espacioPresionado
    jne revisarM
       
    loop revisarMouse
     
    
revisarM: 
    mov ah, 1h   
    int 16h
    jz revisarMouse     
    mov ah, 0h   
    int 16h
    cmp al, revisarZPrograma  
    je zPresionado
    jne revisarMouse
    
    jmp revisarMouse
         

clickIzquierdoPresionado:
    imprimirEnPantalla puntoCodigoMorse
    escribirEnArchivo puntoCodigoMorse
     
 
clickDerechoPresionado:
    imprimirEnPantalla lineaCodigoMorse
    escribirEnArchivo lineaCodigoMorse
    
    
    
zPresionado: 
    imprimirEnPantalla espacioNuevaPalabraCodigoMorse
    escribirEnArchivo espacioNuevaPalabraCodigoMorse  
      
    
 
espacioPresionado: 
    imprimirEnPantalla verEspacioCodigoMorse
    escribirEnArchivo espacioCodigoMorse
    
finalizarPrograma:
    crearElArchivo finalizarConArchivo
    
 
  escribirTxt proc near
   mov ah, 3dh
   mov al, 1
   mov dx, offset crearArchivo
   int 21h
   mov handle, ax
   ret
    
    
end