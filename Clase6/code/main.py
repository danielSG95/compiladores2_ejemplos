from gramatica.gramatica import parse
from symbols.env import Environment

# if
# while -> for

if __name__ == '__main__':
    input = '''
        var suma:number = 2 + 2;
        var suma2:number = 10;
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
        
        var resultado:boolean = false;
        var resultado2:boolean = suma2 > suma;
        
        console.log(resultado2);
        
        console.log(resultado);
        if ( resultado ) {
            var saludo:number = 2*2;
            console.log("el valor es verdadero");
            console.log(saludo);
            if ( true || false ) {
                console.log(mensaje1);
                console.log("si funciono");
            }
        } else { 
            console.log("error "); 
        }
    '''
    global_env = Environment(None)

    parsed = parse(input)
    for instruccion in parsed:
        # print(instruccion)
        instruccion.ejecuta(env=global_env)

  