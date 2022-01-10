import random
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template


class Resolvedor(Agent):
    class perguntaTipoFuncao(OneShotBehaviour):
        async def run(self):
            pergunta = Message(to = "si_sma_receiver_001@jix.im")
            pergunta.set_metadata("performative", "request")
            pergunta.body = "Qual o tipo da funcao?"
            await self.send(pergunta)

            resposta = await self.receive(timeout= 10)
            if resposta:
                print("Grau da equacao: {}".format(resposta.body))
    
    class resolvePrimeiroGrau(CyclicBehaviour):
        k=0
        a=None
        b=None
        x=random.randint(-1000,1000)
        primeiroChute = 0

        async def on_start(self):
            chuteInicial = Message(to= "si_sma_receiver_001@jix.im")
            chuteInicial.set_metadata("performative", "subscribe")
            chuteInicial.body = str(self.primeiroChute)

            self.primeiroChute = self.x

            await self.send(chuteInicial)

        async def run(self):
            resposta = await self.receive(timeout=10)
            if resposta:
                if resposta.body != "primeiro":
                    
                    valor = int(resposta.body)
                    resposta = Message(to= str(resposta.sender))
                    resposta.set_metadata("performative", "subscribe")

                    if valor == 0:
                        print("encontrou zero da funcao para x igual a: {}".format(self.x))
                        self.kill()
                        return

                    elif self.k == 0:
                        self.b = valor
                        resposta.body = str(self.x)
                        await self.send(resposta)


                    elif self.k == 1:
                        self.a = round( (valor - self.b) / self.x )
                        self.x = int(-self.b / self.a)   
                    
                        resposta.body = str( self.x )
                        await self.send(resposta)

                    self.k += 1
            
        async def on_end(self):
            await self.agent.stop()


    async def setup(self):
        self.compPergunta = self.perguntaTipoFuncao()
        tempPergunta = Template()
        tempPergunta.set_metadata("performative", "inform")
        self.add_behaviour(self.compPergunta, tempPergunta)

        compResponder = self.resolvePrimeiroGrau()
        tempResponder = Template()
        tempResponder.set_metadata("performative", "inform")
        self.add_behaviour(compResponder, tempResponder)