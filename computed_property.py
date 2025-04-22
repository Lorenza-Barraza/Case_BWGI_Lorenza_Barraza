#Importando as bibliotecas necessárias:
from math import sqrt

#Definindo o decorator 'computed_property':
class computed_property:
    #Definindo as funções a serem chamadas dentro da classe:
    def __init__(self, *dependencies):      #Instancia a classe quando o decorator é chamado
        self.dependencies = dependencies
        self._fget = None
        self._fset = None
        self._fdel = None
        self.__doc__ = None

    def __call__(self, fget):     #Chamando o objeto como uma função
        self._fget = fget
        self.__doc__ = fget.__doc__
        return self

    def getter(self, fget):     #Acessando os atributos (no caso do exemplo mais adiante, a magnitude) a serem calculados
        self._fget = fget
        self.__doc__ = fget.__doc__
        return self

    def setter(self, fset):     #Atribuindo o valor (no caso do exemplo mais adiante, ao diâmetro), guarda possíveis modificações
        self._fset = fset
        return self

    def deleter(self, fdel):      #Guarda possíveis remoções dos atributos
        self._fdel = fdel
        return self

    def __set_name__(self, owner, name):      #Define os nomes dos atributos usados internamente para armazenar o cache do valor e as dependências da propriedade
        self.name = name
        self.cache_attr = f"_cached_{name}"
        self.deps_attr = f"_deps_{name}"

    def __get__(self, instance, owner=None):      #Ao chamar o valor (no caso do exemplo mais adiante, a magnitude), se o valor já foi calculado e as dependências não mudaram, ele retorna o valor salvo no cache
        if instance is None:
            return self

        current_deps = tuple(getattr(instance, attr, None) for attr in self.dependencies)

        if hasattr(instance, self.cache_attr):
            cached_value = getattr(instance, self.cache_attr)
            cached_deps = getattr(instance, self.deps_attr)
            if cached_deps == current_deps:
                return cached_value

        result = self._fget(instance)
        setattr(instance, self.cache_attr, result)
        setattr(instance, self.deps_attr, current_deps)
        return result

    def __set__(self, instance, value):
        if self._fset is None:
            raise AttributeError(f"Can't set attribute '{self.name}'")      #Na primeira vez que o atributo for chamado, ele não pode ser modificado
        self._fset(instance, value)     #O valor novo é inserido nos atributos a serem calculados (ou recalculados)
        #E o cache e suas dependências salvas são deletadas para garantir que na próxima vez que o atributo for acessado ele será recalculado corretamente
        if hasattr(instance, self.cache_attr):
            delattr(instance, self.cache_attr)
        if hasattr(instance, self.deps_attr):
            delattr(instance, self.deps_attr)

    def __delete__(self, instance):
        if self._fdel is None:
            raise AttributeError(f"Can't delete attribute '{self.name}'")     #Se o método não tiver sido definido, não é possível deletar a propriedade
        self._fdel(instance)
        #Novamente, após o cálculo, o cache e suas dependências salvas são deletadas
        if hasattr(instance, self.cache_attr):
            delattr(instance, self.cache_attr)
        if hasattr(instance, self.deps_attr):
            delattr(instance, self.deps_attr)

#Definindo as classes do exemplo a serem calculadas a partir do decorator:
#Representa um vetor 3D:
class Vector:
    def __init__(self, x, y, z, color=None):
        self.x, self.y, self.z = x, y, z
        self.color = color

    #O método magnitude calcula o módulo do vetor:
    @computed_property('x', 'y', 'z')
    def magnitude(self):
        print('calculando magnitude...')
        return sqrt(self.x**2 + self.y**2 + self.z**2)
#Define um círculo com um padrão de raio=1:
class Circle:
    def __init__(self, radius=1):
        self.radius = radius

    #Define que o diâmetro será sempre o dobro do raio:
    @computed_property('radius')
    def diameter(self):
        """Circle diameter from radius"""
        print('calculando diâmetro...')
        return self.radius * 2

    #Permite recalculado/atualizar o raio se o diâmetro mudar:
    @diameter.setter
    def diameter(self, diameter):
        self.radius = diameter / 2

    #O raio vai para zero se o diâmetro for deletado:
    @diameter.deleter
    def diameter(self):
        self.radius = 0

#Exemplos fornecidos no exercício: vamos calcular a magnitude do vetor e o diâmetro do círculo e printar para o usuário:
print("Testes automáticos com valores fixos:\n")
print("Vetor:")
v = Vector(9, 2, 6)
print(v.magnitude)
v.color = 'red'
print(v.magnitude)
v.y = 18
print(v.magnitude)

print("\nDiâmetro:")
c = Circle()
print(c.diameter)
c.diameter = 10
print(c.radius)
del c.diameter
print(c.radius)

#Interagindo com o usuário:
print("\nInteragindo com o usuário:")

#Vetor
resposta = input("Deseja calcular a magnitude de um vetor? (s/n): ").strip().lower()
if resposta == 's':
    entrada = input("Insira as coordenadas do vetor (exemplo: 9, 2, 6): ").strip()
    try:
        x, y, z = map(float, entrada.split(','))
        v_user = Vector(x, y, z)
        print(f"Magnitude do vetor ({x}, {y}, {z}) = {v_user.magnitude}")
    except ValueError:
        print("Entrada inválida. Use o formato: número, número, número")
else:
    print("Ok, pulando o cálculo da magnitude")

#Círculo
resposta = input("\nDeseja calcular o diâmetro de um círculo? (s/n): ").strip().lower()
if resposta == 's':
    entrada = input("Insira o raio do círculo (exemplo: 5): ").strip()
    try:
        r = float(entrada)
        c_user = Circle(r)
        print(f"Diâmetro do círculo com raio {r} = {c_user.diameter}")
    except ValueError:
        print("Entrada inválida. Use um número como raio")
else:
    print("Ok, pulando o cálculo do diâmetro")
