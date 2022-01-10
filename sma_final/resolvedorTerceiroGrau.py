from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template


class Resolvedor(Agent):
    class resolveSegundoGrau(CyclicBehaviour):
        x = -1000
        async def on_start(self):
            pergunta = Message(to = "si_sma_receiver_001@jix.im")
            pergunta.set_metadata("performative", "request")
            pergunta.body = "Qual o tipo da funcao?"
            await self.send(pergunta)

            resposta = await self.receive(timeout= 10)
            
            if resposta:
                print("Grau da equacao: {}".format(resposta.body))

            pergunta = Message(to= "si_sma_receiver_001@jix.im")
            pergunta.set_metadata("performative", "subscribe")
            primeiroChute = -1000
            pergunta.body = str(primeiroChute)

            await self.send(pergunta)

        async def run(self):
            resposta = await self.receive(timeout=10)
            if resposta:
                if resposta.body == "0":
                    print("encontrou zero da funcao para x igual a: {}".format(self.x))
                    self.kill()
                    return
                self.x += 1
                if self.x > 1000:
                    self.kill()
                    return
                chute = Message(to= str(resposta.sender))
                chute.set_metadata("performative", "subscribe")
                chute.body = str(self.x)
                await self.send(chute)
        
        async def on_end(self):
            await self.agent.stop()

    async def setup(self):
        compResponder = self.resolveSegundoGrau()
        tempResponder = Template()
        tempResponder.set_metadata("performative", "inform")
        self.add_behaviour(compResponder, tempResponder)
