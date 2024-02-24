from gramatica.gramatica import parse
from symbols.env import Environment

if __name__ == '__main__':
    input = '''
        var suma:number = 2 + 2;
        var saludo:string = "Hello World!";
        var mensaje1:string = "OLC2";
        var mensaje2:string = " HOY SI SALE";
        suma = 3 + 2;
        console.log("Hello World!");
        console.log(suma);
        console.log(saludo);
        saludo = "Ya se termino";
        console.log(mensaje1 + mensaje2);
        console.log(2 + 2 - 1);
        console.log(saludo);
    '''
    global_env = Environment()

    parsed = parse(input)
    for instruccion in parsed:
        # print(instruccion)
        instruccion.ejecuta(env=global_env)

  