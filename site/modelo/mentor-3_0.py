# -*- coding: utf-8 -*-
import random
import time
from typing import Dict, List, Optional, Tuple

# --- BASE DE CONHECIMENTO ESTRUTURADA ---
# Agora, cada tópico é uma jornada com passos sequenciais.
BASE_CONHECIMENTO = {
    "produtividade": {
        "sinonimos": ["produzir", "foco", "eficiência", "pomodoro", "organização"],
        "passos": [
            {
                "conselho": "O primeiro passo para a super produtividade é gerenciar sua energia, não apenas seu tempo. Vamos começar com a 'Técnica Pomodoro': trabalhe com foco total por 25 minutos e depois faça uma pausa curta de 5 minutos. Isso mantém sua mente afiada.",
                "pergunta": "Você já tentou usar um cronômetro para gerenciar suas tarefas assim?"
            },
            {
                "conselho": "Ótimo! Agora que você está controlando os sprints de trabalho, vamos priorizar. Use a 'Matriz de Eisenhower': divida suas tarefas entre Urgente/Não Urgente e Importante/Não Importante. Foque no que é Importante, seja urgente ou não.",
                "pergunta": "Isso ajuda a clarear o que você deve fazer a seguir?"
            },
            {
                "conselho": "Excelente. O nível final é o 'Time Blocking'. Em vez de uma lista de tarefas, aloque blocos de tempo específicos no seu calendário para cada atividade importante. 'Das 14h às 15h: Foco total no relatório X'. Isso protege seu tempo e cria compromissos reais.",
                "pergunta": "Pronto para tentar agendar seu próximo dia dessa forma?"
            }
        ],
        "conclusao": "Você completou a jornada da Produtividade! Integrar essas três técnicas fará uma diferença enorme."
    },
    "oratória": {
        "sinonimos": ["falar em público", "apresentação", "discurso", "comunicação"],
        "passos": [
            {
                "conselho": "Para dominar a oratória, o segredo é a estrutura. Antes de pensar nas palavras, defina sua 'Mensagem Central'. Qual é a ÚNICA coisa que você quer que sua audiência lembre? Todo o resto deve servir a essa mensagem.",
                "pergunta": "Você consegue definir a Mensagem Central da sua próxima apresentação em uma única frase?"
            },
            {
                "conselho": "Com a mensagem definida, crie um roteiro simples: 1) Abertura impactante (uma pergunta, um dado surpreendente), 2) Desenvolvimento (3 pontos que suportam sua mensagem) e 3) Fechamento (reforce a mensagem e faça uma chamada para ação).",
                "pergunta": "Essa estrutura parece mais gerenciável do que um texto gigante para decorar?"
            },
            {
                "conselho": "Finalmente, pratique a 'entrega'. Grave a si mesmo falando. Observe sua linguagem corporal, seu tom de voz e suas pausas. A naturalidade vem da prática deliberada, não da decoração. Respire fundo antes de começar!",
                "pergunta": "Você se sente mais confiante para praticar agora?"
            }
        ],
        "conclusao": "Parabéns! Com estrutura e prática, você está no caminho para se tornar um comunicador memorável."
    },
    "aprendizado": {
        "sinonimos": ["aprender", "estudar", "conhecimento", "estudo", "memorizar"],
        "passos": [
            {
                "conselho": "Para aprender de verdade, precisamos ser ativos, não passivos. Comece com a 'Técnica Feynman': pegue um conceito e tente explicá-lo em termos simples, como se fosse para uma criança. Isso revela imediatamente onde estão as lacunas no seu entendimento.",
                "pergunta": "Que tal tentar explicar o último conceito que você estudou agora?"
            },
            {
                "conselho": "Agora vamos solidificar o conhecimento. Use a 'Repetição Espaçada'. Em vez de revisar 10 vezes em um dia, revise uma vez por dia ao longo de várias semanas. Ferramentas como o Anki automatizam isso e são extremamente poderosas para a memória de longo prazo.",
                "pergunta": "Você já usou algum sistema de flashcards para estudar?"
            },
            {
                "conselho": "Por fim, conecte o que você aprendeu com o que você já sabe. Crie analogias, metáforas ou mapas mentais. O conhecimento não deve ficar em 'caixas' isoladas. Quanto mais conexões você criar, mais forte será a retenção.",
                "pergunta": "Consegue pensar em uma analogia para algo que você aprendeu recentemente?"
            }
        ],
        "conclusao": "Fantástico! Com aprendizado ativo, repetição espaçada e conexões, você se tornou um mestre em aprender a aprender."
    }
}


class Topico:
    """ Representa um tópico de conhecimento com sua jornada de aprendizado. """
    def __init__(self, nome, dados):
        self.nome = nome
        self.sinonimos = dados["sinonimos"]
        self.passos = dados["passos"]
        self.conclusao = dados["conclusao"]

    def obter_passo(self, numero_passo: int) -> Optional[Dict]:
        if 0 <= numero_passo < len(self.passos):
            return self.passos[numero_passo]
        return None

class Usuario:
    """ Gerencia o estado e o progresso do usuário. """
    def __init__(self, nome: str):
        self.nome = nome
        self.progresso: Dict[str, int] = {}  # Ex: {"produtividade": 2}

    def obter_passo_atual(self, topico: str) -> int:
        return self.progresso.get(topico, 0)

    def avancar_passo(self, topico: str):
        passo_atual = self.obter_passo_atual(topico)
        self.progresso[topico] = passo_atual + 1

class Mentor:
    """ A inteligência central do TuperAI. """
    def __init__(self):
        self.topicos: List[Topico] = [Topico(nome, dados) for nome, dados in BASE_CONHECIMENTO.items()]
        self.topico_atual: Optional[Topico] = None

    def _encontrar_topico(self, entrada: str) -> Optional[Topico]:
        entrada = entrada.lower()
        # Procura por correspondência exata ou sinônimos
        for topico in self.topicos:
            if entrada == topico.nome or entrada in topico.sinonimos:
                return topico
        return None
    
    def saudar(self, usuario: Usuario) -> str:
        topicos_disponiveis = ", ".join([t.nome for t in self.topicos])
        return (f"\nOlá, {usuario.nome}! É um prazer tê-lo aqui.\n"
                f"Estou pronto para iniciarmos uma jornada de desenvolvimento.\n"
                f"Podemos focar em: **{topicos_disponiveis}**.\n"
                f"Qual área você gostaria de aprimorar hoje?")

    def obter_resposta(self, entrada: str, usuario: Usuario) -> str:
        entrada = entrada.lower()
        comandos_prosseguir = ["próximo", "continue", "sim", "ok", "pode ser"]
        
        # 1. Checar se o usuário quer continuar no tópico atual
        if any(cmd in entrada for cmd in comandos_prosseguir) and self.topico_atual:
            usuario.avancar_passo(self.topico_atual.nome)
        
        # 2. Checar se o usuário quer mudar de tópico
        else:
            topico_encontrado = self._encontrar_topico(entrada)
            if topico_encontrado:
                self.topico_atual = topico_encontrado
            # Se não encontrar tópico e não for comando, a resposta padrão é acionada no final
        
        # 3. Se não há um tópico ativo, pede para o usuário escolher um
        if not self.topico_atual:
            return "Por favor, escolha um dos tópicos de foco para começarmos."

        # 4. Com um tópico ativo, buscar o passo atual e gerar a resposta
        passo_atual_idx = usuario.obter_passo_atual(self.topico_atual.nome)
        passo_info = self.topico_atual.obter_passo(passo_atual_idx)

        if passo_info:
            resposta = (f"Certo, vamos falar sobre **{self.topico_atual.nome.upper()}** (Passo {passo_atual_idx + 1}/{len(self.topico_atual.passos)}).\n\n"
                        f"👉 {passo_info['conselho']}\n\n"
                        f"🤔 {passo_info['pergunta']}\n"
                        f"   (Digite 'próximo' para avançar)")
            return resposta
        else:
            # Usuário concluiu a jornada do tópico
            conclusao = self.topico_atual.conclusao
            self.topico_atual = None # Reseta o tópico para que ele escolha um novo
            return f"✨ **PARABÉNS, {usuario.nome.upper()}!** ✨\n{conclusao}\n\nQue tal escolhermos um novo tópico para desenvolver?"


class SessaoMentoria:
    """ Orquestra a interação completa do usuário com o mentor. """
    def __init__(self):
        self.mentor = Mentor()
        self.usuario = None

    def _display_boas_vindas(self):
        print("=" * 60)
        print("🤖 Bem-vindo ao TuperAI 2.0 - Seu Mentor de Jornada 🚀")
        print("=" * 60)

    def iniciar(self):
        self._display_boas_vindas()
        nome_usuario = input("Para começarmos, como gostaria de ser chamado? ").strip().capitalize()
        self.usuario = Usuario(nome_usuario)
        
        print(self.mentor.saudar(self.usuario))

        while True:
            try:
                entrada = input(f"\n{self.usuario.nome}: ").strip()
                if entrada.lower() in ['sair', 'exit', 'tchau', 'fim']:
                    print(f"\nMentor TuperAI: Até a próxima, {self.usuario.nome}! Lembre-se que o progresso é diário. ✨")
                    break
                
                if not entrada:
                    continue

                resposta_mentor = self.mentor.obter_resposta(entrada, self.usuario)
                
                print("\n" + "---" * 15)
                print(f"Mentor TuperAI: {resposta_mentor}")
                print("---" * 15)

            except (KeyboardInterrupt, EOFError):
                print(f"\n\nMentor TuperAI: Sessão encerrada. Até logo, {self.usuario.nome}!")
                break

if __name__ == "__main__":
    sessao = SessaoMentoria()
    sessao.iniciar()