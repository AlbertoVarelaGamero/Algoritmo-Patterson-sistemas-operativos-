# sardinas_patterson.py
# Implementación del algoritmo Sardinas–Patterson
# Entrada: code = set/list de palabras (strings)
# Salida: True si el código es únicamente decodificable, False si NO lo es.

from typing import Set, List

def suffixes(a: str, b: str) -> Set[str]:
    """
    Si a es prefijo de b, devuelve el sufijo s tal que b = a + s
    Si b es prefijo de a, devuelve el sufijo s tal que a = b + s
    Si ninguno es prefijo del otro, devuelve conjunto vacío.
    """
    res = set()
    if a == b:
        # si son iguales, el sufijo es la cadena vacía
        res.add("")
        return res
    if len(a) <= len(b) and b.startswith(a):
        res.add(b[len(a):])
    if len(b) <= len(a) and a.startswith(b):
        res.add(a[len(b):])
    return res

def sardinas_patterson(code: List[str]) -> bool:
    """
    Devuelve True si el código es únicamente decodificable (UD),
    False si no lo es (es decir, si existe ambigüedad).
    """
    # normalizamos a conjunto y eliminamos duplicados
    C = set(code)
    # U1: todos los sufijos no vacíos que resultan de comparar palabras distintas
    U_prev = set()
    for x in C:
        for y in C:
            if x == y:
                continue
            s = suffixes(x, y)
            # añadimos todos los sufijos, incluido "" si aparece
            for t in s:
                if t != "":  # PD: se puede añadir "" también, pero lo tratamos después
                    U_prev.add(t)
                else:
                    # si aparece la cadena vacía tras comparar dos words -> no UD
                    return False

    # si U1 contiene la cadena vacía -> NO es UD (lo tratamos arriba)
    # iteramos generando U2, U3, ... hasta repetición o hasta detectar ""
    seen = set()  # para detectar loop en conjuntos (usamos tuplas ordenadas)
    while True:
        # si ya vimos este conjunto, se entró en ciclo -> código UD
        key = tuple(sorted(U_prev))
        if key in seen:
            return True  # no apareció la cadena vacía y se repite -> UD
        seen.add(key)

        U_next = set()
        # regla: U_{i+1} = sufijos(C, U_i) U sufijos(U_i, C)
        # (donde sufijos(A,B) es el conjunto de sufijos de comparar cada a in A con b in B)
        # además si en cualquier comparación aparece "" -> no UD (return False)
        for a in C:
            for b in U_prev:
                s = suffixes(a, b)
                if "" in s:
                    return False
                U_next.update(s)
        for a in U_prev:
            for b in C:
                s = suffixes(a, b)
                if "" in s:
                    return False
                U_next.update(s)

        # eliminamos cadenas vacías si se hubieran colado (por seguridad)
        if "" in U_next:
            return False

        # si U_next es vacío y no apareció "" y no hay repetición, entonces UD
        if not U_next:
            return True

        U_prev = U_next


# Ejemplo rápido
if __name__ == "__main__":
    codes = [
        (["1", "01", "011"], False),  # ejemplo no UD (contradictorio)
        (["0", "10", "110"], True),   # ejemplo UD
        (["a", "ab", "ba"], False)    # posiblemente no UD
    ]
    for code, expected in codes:
        res = sardinas_patterson(code)
        print(f"Código: {code} -> únicamente decodificable? {res} (esperado {expected})")
