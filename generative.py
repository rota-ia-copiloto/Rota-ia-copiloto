
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class GenerativeLayerError(RuntimeError):
    pass

class MeetingQuestion(BaseModel):
    theme: str = Field(
        description="Tema curto da pergunta, por exemplo: Linha de base, Decisão, Dados, Experimento, Atores ou Alternativas."
    )
    question: str = Field(
        description="Pergunta aberta, específica ao caso e útil para a próxima reunião do facilitador."
    )
    why_it_matters: str = Field(
        description="Explicação curta, em uma frase, sobre por que essa pergunta é relevante."
    )

class MeetingGuide(BaseModel):
    meeting_objective: str = Field(
        description="Objetivo prático da próxima reunião, em no máximo duas frases."
    )
    opening_question: str = Field(
        description="Uma pergunta de abertura que ajude o município a começar pelo problema, não pela tecnologia."
    )
    questions: List[MeetingQuestion] = Field(
        description="De 5 a 7 perguntas contextuais, não redundantes, para a reunião."
    )
    closing_decision: str = Field(
        description="Qual decisão ou evidência a reunião deve permitir ao final."
    )
    facilitator_caution: str = Field(
        description="Um cuidado metodológico específico para o facilitador neste caso."
    )

SYSTEM_INSTRUCTION = """
Você é a camada generativa de um copiloto de facilitação para um programa de transformação digital
e inteligência artificial em governos locais.

Sua função NÃO é aprovar, reprovar ou autorizar projetos.
Sua função é ajudar o facilitador a preparar uma conversa melhor com o município.

Princípios obrigatórios:
1. Comece pelo problema público ou administrativo, não pela tecnologia.
2. Não presuma que IA é necessária.
3. Não faça perguntas cuja resposta já esteja claramente informada no relato ou nos campos estruturados.
4. Priorize lacunas que mudariam uma decisão: linha de base, fluxo decisório, dados, atores, hipótese e limites do experimento.
5. Quando houver dados sensíveis, alto impacto, decisão automatizada ou supervisão humana incerta, formule perguntas que aumentem a compreensão e a governança; não dê parecer jurídico.
6. Não solicite ao usuário que cole dados pessoais, prontuários, nomes, documentos sigilosos ou informações confidenciais.
7. Diferencie apoio à decisão de decisão automatizada.
8. Formule perguntas abertas, concretas e utilizáveis numa reunião real.
9. Evite jargão e perguntas genéricas.
10. A decisão final permanece humana.

A jornada metodológica disponível é:
DIAGNOSTICAR → CO-DESENHAR → IMPLEMENTAR → AVALIAR → COMUNICAR.

A classificação de estágio e prioridade já foi feita por regras explícitas.
Você NÃO deve alterá-la; apenas use-a como contexto para formular o roteiro.
"""

def _compact_case(structured_case: Dict[str, Any]) -> str:
    labels = {
        "area":"Área", "estagio":"Estágio declarado", "problema":"Problema estruturado",
        "solucao":"Uso de IA considerado", "processo":"Processo atual", "gargalo":"Gargalo",
        "criterios":"Critérios formalizados", "indicador":"Linha de base/indicador",
        "resultado":"Resultado pretendido", "papel":"Papel da IA", "decisor_atual":"Decisor atual",
        "decisor_futuro":"Decisor futuro", "revisao":"Revisão humana", "contrariar":"Pode contrariar IA",
        "impacto":"Impacto de erro", "pessoais":"Dados pessoais", "sensiveis":"Dados sensíveis",
        "origem_dados":"Origem dos dados", "fornecedor":"Fornecedor externo",
        "dados_fora":"Dados fora do ambiente municipal", "hipotese":"Hipótese do experimento",
        "escopo":"Menor escopo", "indicador_teste":"Indicador de sucesso",
        "parada":"Critério de parada", "reversivel":"Reversibilidade"
    }
    parts = []
    for key, label in labels.items():
        value = structured_case.get(key)
        if value not in (None, ""):
            parts.append(f"- {label}: {value}")
    return "\n".join(parts)

def generate_meeting_guide(
    api_key: str,
    model_name: str,
    narrative: str,
    structured_case: Dict[str, Any],
    deterministic_result: Dict[str, Any],
    fallback_plan: Dict[str, Any],
) -> MeetingGuide:
    if not api_key:
        raise GenerativeLayerError("API key não configurada.")

    if not narrative.strip():
        raise GenerativeLayerError("O relato livre está vazio.")

    client = genai.Client(api_key=api_key)

    evidence_lines = []
    for name, value in deterministic_result.get("evidence", {}).items():
        status, reason = value
        evidence_lines.append(f"- {name}: {status} — {reason}")

    prompt = f"""
RELATO LIVRE DO FACILITADOR
{narrative.strip()}

INFORMAÇÕES ESTRUTURADAS JÁ DISPONÍVEIS
{_compact_case(structured_case) or "- Nenhuma informação estruturada adicional."}

LEITURA DETERMINÍSTICA DO COPILOTO
- Estágio sugerido: {deterministic_result.get("suggested")}
- Prioridade de atenção: {deterministic_result.get("attention")}
- Leitura principal: {deterministic_result.get("main")}

SITUAÇÃO DAS QUATRO EVIDÊNCIAS
{chr(10).join(evidence_lines)}

LACUNAS JÁ IDENTIFICADAS
{chr(10).join("- " + x for x in deterministic_result.get("gaps", []))}

ATORES JÁ SUGERIDOS
{chr(10).join("- " + x for x in deterministic_result.get("actors", []))}

ROTEIRO-BASE DETERMINÍSTICO
- Objetivo: {fallback_plan.get("objetivo")}
- Próximo movimento: {fallback_plan.get("movimento")}
- Entregável: {fallback_plan.get("entregavel")}

TAREFA
Produza um roteiro para a PRÓXIMA reunião do facilitador.
Gere de 5 a 7 perguntas.
Não repita perguntas cujas respostas já estejam claras.
As perguntas devem ajudar a preencher as lacunas que realmente mudam o próximo movimento.
Se o relato estiver incompleto, use isso como motivo para perguntas de diagnóstico.
Se houver uma hipótese de IA desnecessariamente complexa, inclua uma pergunta sobre alternativas mais simples.
Escreva em português brasileiro, de forma humana, direta e profissional.
"""

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.25,
                response_mime_type="application/json",
                response_schema=MeetingGuide,
            ),
        )

        if not response.text:
            raise GenerativeLayerError("O modelo não retornou conteúdo.")

        return MeetingGuide.model_validate_json(response.text)

    except GenerativeLayerError:
        raise
    except Exception as exc:
        raise GenerativeLayerError(
            "Não foi possível gerar o roteiro com a camada generativa. "
            "Verifique a API key, o nome do modelo e a disponibilidade da API. "
            f"Detalhe técnico: {exc}"
        ) from exc
