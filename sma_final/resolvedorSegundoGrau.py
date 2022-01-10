from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template


class Resolvedor(Agent):    
    class resolveSegundoGrau(CyclicBehaviour):
        x0 = 1000
        x1 = -1000
        p = round((x0 + x1) / 2)
        res_x = None
        res_p = None
        k=0

        async def on_start(self):
            pergunta = Message(to = "si_sma_receiver_001@jix.im")
            pergunta.set_metadata("performative", "request")
            pergunta.body = "Qual o tipo da funcao?"
            
            await self.send(pergunta)
            resposta = await self.receive(timeout= 10)

            if resposta:
                print("Grau da equacao: {}".format(resposta.body))


        async def run(self):
            resposta = await self.receive(timeout=10)
            if resposta:
                if resposta.body == "0":
                    print("encontrou zero da funcao para x igual a: {}".format(self.x1))
                    self.kill()
                    return
                self.x1 += 1
                if self.x1 > 1000:
                    self.kill()
                    return
                resposta = Message(to=str(resposta.sender))
                resposta.set_metadata("performative", "subscribe")
                resposta.body = str(self.x1)

                await self.send(resposta)


            else:
                mensagem = Message(to="si_sma_receiver_001@jix.im")
                mensagem.set_metadata("performative", "subscribe")
                mensagem.body = str(self.p)

                await self.send(mensagem)
                

                    


    async def setup(self):
        compResponder = self.resolveSegundoGrau()
        tempResponder = Template()
        tempResponder.set_metadata("performative", "inform")
        self.add_behaviour(compResponder, tempResponder)








