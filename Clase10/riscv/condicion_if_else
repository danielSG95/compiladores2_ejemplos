.data
msg1: .asciz "Se cumple la condicion\n"
msg2: .asciz "No se cumple la condicion\n"
msg3: .asciz "else if se cumple\n"
.text
.globl main
main:
    # asumiendo valores en a0 y a1
    li t1, 5        # a0 = 5
    li t2, 10       # a1 = 10
    li t3, 2
    blt t2, t1, if_part   # si a0 < a1, ejecuta if_part
    j else_if           # salta a else_part
if_part:
    # Código del bloque if aquí
    la a1, msg1
    jal ra, print
    j endif
else_if:
    # Código del bloque else aquí
    blt t3, t1, if_part2
    j else
    
if_part2:
	la a1, msg3
    jal ra, print
    j endif
else:
	la a1, msg1
    jal ra, print
    j endif
print:
	li a0, 1
	li a2, 25
	li a7, 64
	ecall
	ret
endif:
