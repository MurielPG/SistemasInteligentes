import time, random, my_lib
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import resolvedorPrimeiroGrau
import resolvedorSegundoGrau
import resolvedorTerceiroGrau


class Gerador(Agent):
    tipos = "primeiro", "segundo", "terceiro"    
    tipoEquacao = random.choice(tipos)
    a=None
    b=None
    c=None
    d=None
    x=None
    if tipoEquacao == "primeiro":
        a,b,x = my_lib.gera_1g()
        print("a:{}   b:{}   x:{}".format(a,b,x) )
    elif tipoEquacao == "segundo":
        a,b,c,x = my_lib.gera_2g()
        print("a:{}   b:{}   c:{}   x:{}".format(a,b,c,x) )
    elif tipoEquacao == "terceiro":
        a,b,c,d,x = my_lib.gera_3g()
        print("a:{}   b:{}   c:{}   d:{}   x:{}".format(a,b,c,d,x) )
        
    class informaFuncao(CyclicBehaviour):
        async def run(self):
            pergunta = await self.receive(timeout= 10)
            if pergunta:
                pergunta = Message(to="si_sma_ex_001@jix.im")
                pergunta.set_metadata("performative", "inform")
                pergunta.body = str( Gerador.tipoEquacao )

                await self.send(pergunta)
                self.kill()
    
    class Calculador(CyclicBehaviour):
        async def run(self):
            chute = await self.receive(timeout= 10)
            if chute:
                x = int(float(chute.body))

                if Gerador.tipoEquacao == "primeiro":
                    raiz = round(Gerador.a*x + Gerador.b)

                elif Gerador.tipoEquacao == "segundo":
                    raiz = round(Gerador.a*x**2 + Gerador.b*x + Gerador.c)

                elif Gerador.tipoEquacao == "terceiro":
                    raiz = round(Gerador.a*x**3 + Gerador.b*x**2 + Gerador.c*x + Gerador.d)
                
                chute = Message(to = str(chute.sender))
                chute.set_metadata("performative", "inform")
                chute.body = str(raiz)

                await self.send(chute)


    async def setup(self):
        compInformar = self.informaFuncao()
        tempInformar = Template()
        tempInformar.set_metadata("performative", "request")
        self.add_behaviour(compInformar, tempInformar)

        compCalculador = self.Calculador()
        tempCalculador = Template()
        tempCalculador.set_metadata("performative", "subscribe")   
        self.add_behaviour(compCalculador, tempCalculador) 



agenteGerador = Gerador("si_sma_receiver_001@jix.im", "~38h[4SmFN")
futur1 = agenteGerador.start()
futur1.result()

if agenteGerador.tipoEquacao == "primeiro":
    agenteResolvedor = resolvedorPrimeiroGrau.Resolvedor("si_sma_ex_001@jix.im", "~38h[4SmFN")
    futur2 = agenteResolvedor.start()
    futur2.result()

elif agenteGerador.tipoEquacao == "segundo":
    agenteResolvedor = resolvedorSegundoGrau.Resolvedor("si_sma_ex_001@jix.im", "~38h[4SmFN")
    futur2 = agenteResolvedor.start()
    futur2.result()

elif agenteGerador.tipoEquacao == "terceiro":
    agenteResolvedor = resolvedorTerceiroGrau.Resolvedor("si_sma_ex_001@jix.im", "~38h[4SmFN")
    futur2 = agenteResolvedor.start()
    futur2.result()


while agenteGerador.is_alive():
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        agenteGerador.stop()
        break
