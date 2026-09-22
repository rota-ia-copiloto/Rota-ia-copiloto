
import streamlit as st
from generative import generate_meeting_guide, GenerativeLayerError

st.set_page_config(page_title="Rota IA", page_icon="🧭", layout="wide")

# ============================================================
# CASOS DE DEMONSTRAÇÃO
# ============================================================
CASES = {
    "A": {
        "municipio":"Município A","area":"Gestão interna","estagio":"Já em uso",
        "relato_livre":"Um servidor municipal já utiliza uma ferramenta pessoal de IA generativa, fora dos sistemas oficiais, para redigir ofícios e memorandos internos. O facilitador quer saber se deve orientar a interrupção ou se o uso pode ser qualificado e institucionalizado.",
        "problema":"Reduzir tempo gasto na elaboração de ofícios e memorandos internos.",
        "solucao":"Servidor utiliza ferramenta pessoal de IA generativa fora dos sistemas oficiais.",
        "processo":"Produção manual de documentos administrativos.","gargalo":"Tempo gasto em tarefas repetitivas.",
        "criterios":"Parcialmente","indicador":"","resultado":"Reduzir tempo de produção de documentos.",
        "papel":"Gerar conteúdo/rascunho","decisor_atual":"Servidor responsável","decisor_futuro":"Servidor responsável",
        "revisao":"Incerto","contrariar":"Sim","impacto":"Média",
        "pessoais":"Não sei","sensiveis":"Não sei","origem_dados":"Documentos administrativos",
        "fornecedor":"Sim","dados_fora":"Não sei",
        "hipotese":"","escopo":"","indicador_teste":"","parada":"","reversivel":"Sim"
    },
    "B": {
        "municipio":"Município B","area":"Saúde","estagio":"Em desenho",
        "relato_livre":"A Secretaria de Saúde quer usar IA para priorizar uma fila de atendimento cruzando dados de prontuários eletrônicos. Ainda não existe protocolo de proteção de dados definido e não está claro se a IA recomendaria ou decidiria a prioridade.",
        "problema":"Melhorar a priorização de uma fila de atendimento em saúde.",
        "solucao":"Usar IA com dados de prontuários eletrônicos para recomendar prioridades.",
        "processo":"","gargalo":"Tempo de espera e dificuldade de priorização.",
        "criterios":"Não sei","indicador":"","resultado":"Reduzir espera e melhorar a priorização.",
        "papel":"Priorizar","decisor_atual":"","decisor_futuro":"",
        "revisao":"Incerto","contrariar":"Incerto","impacto":"Alta",
        "pessoais":"Sim","sensiveis":"Sim","origem_dados":"Prontuário eletrônico",
        "fornecedor":"Não sei","dados_fora":"Não sei",
        "hipotese":"","escopo":"","indicador_teste":"","parada":"","reversivel":"Não sei"
    },
    "C": {
        "municipio":"Município C","area":"Atendimento ao cidadão","estagio":"Ideia / relato inicial",
        "relato_livre":"O município deseja construir um chatbot para responder dúvidas sobre dias e horários da coleta de lixo e pede indicação de conteúdo de capacitação para sua equipe técnica.",
        "problema":"Facilitar o acesso a informações sobre dias e horários da coleta de lixo.",
        "solucao":"Construir um chatbot para responder dúvidas frequentes.",
        "processo":"Informações divulgadas em canais dispersos.","gargalo":"Dificuldade de localizar informação.",
        "criterios":"Sim","indicador":"Volume de dúvidas repetitivas.","resultado":"Reduzir dúvidas repetitivas.",
        "papel":"Informar","decisor_atual":"Não há decisão relevante","decisor_futuro":"Não há decisão relevante",
        "revisao":"Sim","contrariar":"Não se aplica","impacto":"Baixa",
        "pessoais":"Não","sensiveis":"Não","origem_dados":"Calendário e rotas públicas",
        "fornecedor":"Não sei","dados_fora":"Não sei",
        "hipotese":"Uma solução digital simples reduzirá dúvidas repetitivas.","escopo":"Um bairro",
        "indicador_teste":"Redução de dúvidas repetitivas.","parada":"Respostas incorretas recorrentes.","reversivel":"Sim"
    },
    "D": {
        "municipio":"Município D","area":"Jurídico","estagio":"Em desenho",
        "relato_livre":"A assessoria jurídica sugere usar IA generativa para elaborar rascunhos de resposta a pedidos de acesso à informação, buscando reduzir prazos. A decisão administrativa continuaria com a equipe responsável, mas o desenho do fluxo ainda precisa ser detalhado.",
        "problema":"Reduzir tempo de elaboração de respostas a pedidos de acesso à informação.",
        "solucao":"Usar IA generativa para produzir rascunhos de respostas.",
        "processo":"Respostas produzidas manualmente.","gargalo":"Tempo de redação e organização.",
        "criterios":"Sim","indicador":"Prazo médio de resposta.","resultado":"Reduzir tempo mantendo qualidade.",
        "papel":"Gerar conteúdo/rascunho","decisor_atual":"Servidor responsável","decisor_futuro":"Servidor responsável",
        "revisao":"Sim","contrariar":"Sim","impacto":"Média",
        "pessoais":"Sim","sensiveis":"Não sei","origem_dados":"Pedidos de LAI e documentos administrativos",
        "fornecedor":"Não sei","dados_fora":"Não sei",
        "hipotese":"Rascunhos podem reduzir tempo sem transferir a decisão administrativa.",
        "escopo":"Pedidos de baixa complexidade","indicador_teste":"Tempo de elaboração e taxa de correção.",
        "parada":"Omissão, erro relevante ou exposição indevida.","reversivel":"Sim"
    },
    "E": {
        "municipio":"Município E","area":"Obras/Infraestrutura","estagio":"Ideia / relato inicial",
        "relato_livre":"O facilitador ouviu falar de um sistema em outro município que identifica buracos nas ruas a partir de fotografias, mas não sabe se está em operação, quem fornece a tecnologia, quais dados utiliza ou que resultados produziu.",
        "problema":"Possível melhoria da identificação de buracos em vias públicas.",
        "solucao":"Relato de sistema que identificaria buracos por fotografias, sem detalhes.",
        "processo":"","gargalo":"","criterios":"Não sei","indicador":"","resultado":"",
        "papel":"Ainda não está claro","decisor_atual":"","decisor_futuro":"",
        "revisao":"Incerto","contrariar":"Incerto","impacto":"Baixa",
        "pessoais":"Não sei","sensiveis":"Não sei","origem_dados":"Fotografias, origem desconhecida",
        "fornecedor":"Não sei","dados_fora":"Não sei",
        "hipotese":"","escopo":"","indicador_teste":"","parada":"","reversivel":"Não sei"
    }
}

def init():
    st.session_state.setdefault("case", {})
    st.session_state.setdefault("result", None)
    st.session_state.setdefault("meeting_guide", None)

init()

def set_case(k):
    st.session_state.case = CASES[k].copy()
    st.session_state.result = None
    st.session_state.meeting_guide = None

def select_value(label, options, key):
    value = st.session_state.case.get(key, "")
    idx = options.index(value) if value in options else 0
    return st.selectbox(label, options, index=idx, key=f"w_{key}")

def text_value(label, key, height=None, placeholder=None):
    value = st.session_state.case.get(key, "")
    if height:
        return st.text_area(label, value=value, height=height, placeholder=placeholder, key=f"w_{key}")
    return st.text_input(label, value=value, placeholder=placeholder, key=f"w_{key}")

def empty(v):
    return not str(v or "").strip()

# ============================================================
# REGRAS DETERMINÍSTICAS
# ============================================================
def evaluate(d):
    score = 0
    alerts, gaps, actors, known = [], [], [], []

    if d["estagio"] == "Já em uso":
        score += 4
        alerts.append("O uso já está ocorrendo: há exposição atual.")
    elif d["estagio"] == "Piloto":
        score += 3
    elif d["estagio"] == "Em desenho":
        score += 2
    else:
        score += 1

    if d["sensiveis"] == "Sim":
        score += 5
        alerts.append("Há indicação de dados pessoais sensíveis.")
        actors.append("Proteção de dados / encarregado")
    elif d["sensiveis"] == "Não sei":
        gaps.append("Confirmar se existem dados pessoais sensíveis.")

    if d["pessoais"] == "Sim":
        score += 2
    elif d["pessoais"] == "Não sei":
        gaps.append("Confirmar se existem dados pessoais.")

    if d["impacto"] == "Alta":
        score += 4
        alerts.append("Um erro pode gerar consequência relevante.")
    elif d["impacto"] == "Média":
        score += 2

    risky_role = d["papel"] in ["Recomendar", "Priorizar", "Decidir automaticamente"]
    if d["papel"] == "Decidir automaticamente":
        score += 4
        alerts.append("A IA poderá decidir automaticamente.")
    elif d["papel"] in ["Recomendar", "Priorizar"]:
        score += 2

    if risky_role and d["revisao"] != "Sim":
        score += 3
        alerts.append("A supervisão humana é ausente ou incerta.")

    if d["reversivel"] == "Não":
        score += 3
        alerts.append("A intervenção apresenta baixa reversibilidade.")
    elif d["reversivel"] in ["Parcialmente", "Não sei"]:
        score += 1

    if d["fornecedor"] == "Sim" and d["dados_fora"] in ["Sim", "Não sei"]:
        score += 2
        alerts.append("Há fornecedor externo e o fluxo de dados precisa ser esclarecido.")
        actors.append("TI / segurança da informação")

    miss_baseline = sum([
        empty(d["processo"]), empty(d["gargalo"]),
        d["criterios"] in ["", "Não sei"], empty(d["indicador"]), empty(d["resultado"])
    ])
    if miss_baseline >= 3:
        baseline = ("🔴 Incompleta", "Faltam elementos para comparar a situação atual com resultados futuros.")
        gaps.append("Completar a linha de base do processo.")
    elif miss_baseline >= 1:
        baseline = ("🟡 Parcial", "Existe leitura inicial, mas ainda há lacunas.")
    else:
        baseline = ("🟢 Suficiente", "Processo, gargalo e resultado esperado estão identificados.")

    miss_decision = sum([
        d["papel"] in ["", "Ainda não está claro"], empty(d["decisor_atual"]),
        empty(d["decisor_futuro"]), d["revisao"] in ["", "Incerto"], d["contrariar"] in ["", "Incerto"]
    ])
    if miss_decision >= 3:
        decision = ("🔴 Incompleto", "Ainda não está claro como a IA altera o fluxo decisório.")
        gaps.append("Mapear onde a IA entra e quem mantém responsabilidade decisória.")
    elif miss_decision >= 1:
        decision = ("🟡 Parcial", "O fluxo decisório está parcialmente definido.")
    else:
        decision = ("🟢 Suficiente", "Papel da IA e responsabilidade humana estão explicitados.")

    miss_data = sum([
        d["pessoais"] in ["", "Não sei"], d["sensiveis"] in ["", "Não sei"],
        empty(d["origem_dados"]), d["fornecedor"] in ["", "Não sei"], d["dados_fora"] in ["", "Não sei"]
    ])
    critical_data = d["sensiveis"] == "Sim" and (
        d["dados_fora"] in ["Sim", "Não sei"] or d["fornecedor"] in ["Sim", "Não sei"]
    )
    if critical_data:
        datamap = ("🔴 Crítico", "Dados sensíveis combinados com fluxo externo ou ainda não esclarecido.")
        gaps.append("Mapear origem, circulação, acesso e compartilhamento dos dados.")
    elif miss_data >= 3:
        datamap = ("🔴 Incompleto", "O fluxo de dados ainda não está suficientemente compreendido.")
        gaps.append("Completar o mapa dos dados.")
    elif miss_data >= 1:
        datamap = ("🟡 Parcial", "Há informação relevante, mas o fluxo ainda precisa ser completado.")
    else:
        datamap = ("🟢 Suficiente", "Origem, natureza e circulação dos dados estão identificadas.")

    miss_exp = sum([
        empty(d["hipotese"]), empty(d["escopo"]), empty(d["indicador_teste"]),
        empty(d["parada"]), d["reversivel"] in ["", "Não sei"]
    ])
    if miss_exp >= 4:
        experiment = ("⚪ Ainda não aplicável", "O caso ainda não está maduro para desenho de experimento.")
    elif miss_exp >= 2:
        experiment = ("🟡 Parcial", "Hipótese, indicador ou limites do teste ainda precisam ser definidos.")
    else:
        experiment = ("🟢 Suficiente", "Há elementos mínimos para discutir um teste controlado.")

    red = any(x[0].startswith("🔴") for x in [baseline, decision, datamap])
    yellow = any(x[0].startswith("🟡") for x in [baseline, decision, datamap, experiment])

    if red:
        suggested = "Diagnosticar"
        main = (
            "O caso parece ter avançado mais rápido que sua compreensão institucional. "
            "Complete o diagnóstico antes de discutir implementação."
        )
    elif yellow or experiment[0].startswith("⚪"):
        suggested = "Co-desenhar"
        main = (
            "O problema está parcialmente qualificado, mas ainda faltam definições "
            "para uma intervenção testável e proporcional."
        )
    else:
        suggested = "Implementar"
        main = (
            "Há elementos mínimos para discutir um piloto controlado, "
            "com indicadores e critérios de interrupção."
        )

    attention = "Alta" if score >= 13 else ("Média" if score >= 7 else "Baixa")

    actors += ["Facilitador RIL", "Responsável municipal pelo processo"]
    if d["area"]:
        actors.append(f"Área responsável: {d['area']}")
    if risky_role:
        actors.append("Responsável técnico/administrativo pela decisão")
    if d["pessoais"] == "Sim" or d["sensiveis"] == "Sim":
        actors.append("Jurídico / governança")
    actors = list(dict.fromkeys(actors))

    if d["problema"]:
        known.append(f"Problema relatado: {d['problema']}")
    if d["resultado"]:
        known.append(f"Resultado pretendido: {d['resultado']}")
    if d["papel"]:
        known.append(f"Papel pretendido da IA: {d['papel']}")
    if d["estagio"] == "Já em uso":
        known.append("A prática já está em uso.")
    if not known:
        known.append("Ainda há pouca informação estruturada.")

    if not alerts:
        alerts.append("Nenhum sinal crítico evidente com as informações atuais.")

    return {
        "score": score,
        "attention": attention,
        "suggested": suggested,
        "main": main,
        "evidence": {
            "Linha de base": baseline,
            "Mapa da decisão": decision,
            "Mapa dos dados": datamap,
            "Experimento": experiment,
        },
        "alerts": list(dict.fromkeys(alerts)),
        "gaps": list(dict.fromkeys(gaps)) or ["Validar as informações registradas com a equipe municipal."],
        "actors": actors,
        "known": known,
    }

def facilitation_plan(d, r):
    if r["suggested"] == "Diagnosticar":
        return {
            "objetivo":"Compreender o processo atual e produzir uma linha de base confiável antes de discutir a solução tecnológica.",
            "movimento":"Realizar uma oficina de diagnóstico com os responsáveis pelo processo.",
            "entregavel":"Linha de base + mapa inicial da decisão + mapa inicial dos dados.",
            "perguntas":[
                "Qual problema concreto queremos alterar?",
                "Como o processo funciona hoje e onde está o gargalo?",
                "Quem decide atualmente e com quais critérios?",
                "Que dados são realmente necessários para compreender o problema?",
                "Qual indicador representa a situação atual?"
            ],
            "decisao":"Decidir se o caso está suficientemente compreendido para avançar ao co-desenho."
        }
    if r["suggested"] == "Co-desenhar":
        return {
            "objetivo":"Transformar o diagnóstico em uma hipótese de intervenção clara, proporcional e testável.",
            "movimento":"Conduzir uma oficina de co-desenho com áreas técnicas, decisores e atores afetados.",
            "entregavel":"Mapa da solução + papéis + dados necessários + hipótese de experimento + critérios de sucesso e parada.",
            "perguntas":[
                "A IA é realmente necessária ou uma solução mais simples resolveria?",
                "Onde a IA entraria e qual decisão influenciaria?",
                "Quem mantém responsabilidade humana real?",
                "Qual é o menor experimento reversível possível?",
                "O que justificaria avançar e o que faria o piloto parar?"
            ],
            "decisao":"Decidir se existe desenho suficientemente maduro para um piloto controlado."
        }
    return {
        "objetivo":"Preparar um piloto controlado com responsabilidades, indicadores e salvaguardas explícitas.",
        "movimento":"Planejar implementação em pequena escala e monitoramento desde o início.",
        "entregavel":"Plano de piloto + indicadores + responsáveis + critérios de interrupção.",
        "perguntas":[
            "Qual é a hipótese exata do piloto?",
            "Qual será o menor escopo inicial?",
            "Quais indicadores serão acompanhados?",
            "Quem revisará resultados e incidentes?",
            "Quais condições devem existir antes de ampliar a escala?"
        ],
        "decisao":"Decidir, com base nas evidências, se a iniciativa deve ser ajustada, interrompida ou ampliada."
    }

# ============================================================
# INTERFACE
# ============================================================
st.title("🧭 Rota IA")
st.subheader("Copiloto de Diagnóstico e Co-desenho para Governos Locais")
st.caption("Antes de perguntar qual IA usar, ajude o município a entender o problema que precisa resolver.")
st.warning("MVP demonstrativo: não inserir dados pessoais, sensíveis ou informações confidenciais.")

with st.sidebar:
    st.header("Casos de demonstração")
    for k in ["A", "B", "C", "D", "E"]:
        if st.button(f"Carregar Caso {k}", use_container_width=True):
            set_case(k)
            st.rerun()

    if st.button("Limpar", use_container_width=True):
        st.session_state.case = {}
        st.session_state.result = None
        st.session_state.meeting_guide = None
        st.rerun()

    st.divider()
    st.subheader("Camada generativa")

    try:
        secret_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        secret_key = ""

    try:
        secret_model = st.secrets["GEMINI_MODEL"]
    except Exception:
        secret_model = ""

    if secret_key:
        st.success("API Gemini configurada via Secrets.")
        api_key = secret_key
    else:
        api_key = st.text_input(
            "Gemini API key",
            type="password",
            help="Usada somente nesta sessão. Para publicação, prefira Streamlit Secrets."
        )

    model_name = st.text_input(
        "Modelo",
        value=secret_model or "gemini-2.5-flash-lite",
        help="O modelo pode ser alterado sem mexer no código."
    )

    st.caption(
        "As regras críticas continuam determinísticas. "
        "A camada generativa formula perguntas e roteiro de reunião."
    )

st.header("1. Conte o caso")

relato_livre = text_value(
    "Relato livre do facilitador",
    "relato_livre",
    150,
    "Cole aqui a situação como ela chegou ao facilitador, em linguagem natural."
)

col1, col2 = st.columns(2)
with col1:
    municipio = text_value("Município", "municipio")
    area = select_value(
        "Área responsável",
        ["", "Saúde", "Educação", "Jurídico", "Tecnologia/TI", "Obras/Infraestrutura",
         "Atendimento ao cidadão", "Gestão interna", "Outra"],
        "area"
    )
with col2:
    estagio = select_value(
        "Estágio declarado pelo município",
        ["", "Ideia / relato inicial", "Em desenho", "Piloto", "Já em uso"],
        "estagio"
    )

problema = text_value(
    "Qual problema público ou administrativo o município está tentando resolver?",
    "problema", 110, "Descreva o problema antes da solução tecnológica."
)
solucao = text_value(
    "Que uso de IA está sendo considerado ou já utilizado?",
    "solucao", 85
)

st.header("2. Quatro evidências para qualificar o caso")
t1, t2, t3, t4 = st.tabs(
    ["1️⃣ Linha de base", "2️⃣ Mapa da decisão", "3️⃣ Mapa dos dados", "4️⃣ Experimento"]
)

with t1:
    processo = text_value("Como o processo funciona atualmente?", "processo", 90)
    gargalo = text_value("Onde está o principal gargalo?", "gargalo")
    criterios = select_value("Há critérios atuais formalizados?", ["", "Sim", "Parcialmente", "Não", "Não sei"], "criterios")
    indicador = text_value("Existe uma linha de base / indicador atual?", "indicador")
    resultado = text_value("Que resultado queremos mudar?", "resultado")

with t2:
    papel = select_value(
        "Papel pretendido da IA",
        ["", "Informar", "Gerar conteúdo/rascunho", "Recomendar", "Priorizar", "Decidir automaticamente", "Ainda não está claro"],
        "papel"
    )
    decisor_atual = text_value("Quem decide hoje?", "decisor_atual")
    decisor_futuro = text_value("Quem decidiria depois?", "decisor_futuro")
    revisao = select_value("Há revisão humana real?", ["", "Sim", "Não", "Incerto"], "revisao")
    contrariar = select_value(
        "A pessoa responsável pode contrariar a recomendação da IA?",
        ["", "Sim", "Não", "Incerto", "Não se aplica"],
        "contrariar"
    )
    impacto = select_value("Consequência de um erro", ["", "Baixa", "Média", "Alta"], "impacto")

with t3:
    pessoais = select_value("Há dados pessoais?", ["", "Sim", "Não", "Não sei"], "pessoais")
    sensiveis = select_value("Há dados pessoais sensíveis?", ["", "Sim", "Não", "Não sei"], "sensiveis")
    origem_dados = text_value("Qual é a origem principal dos dados?", "origem_dados")
    fornecedor = select_value("Há fornecedor ou ferramenta externa?", ["", "Sim", "Não", "Não sei"], "fornecedor")
    dados_fora = select_value("Os dados saem ou podem sair do ambiente municipal?", ["", "Sim", "Não", "Não sei"], "dados_fora")

with t4:
    hipotese = text_value("Hipótese do experimento", "hipotese", 80)
    escopo = text_value("Qual seria o menor escopo de teste possível?", "escopo")
    indicador_teste = text_value("Qual indicador mostraria melhora?", "indicador_teste")
    parada = text_value("Qual evidência faria o piloto ser interrompido?", "parada")
    reversivel = select_value("O experimento é reversível?", ["", "Sim", "Parcialmente", "Não", "Não sei"], "reversivel")

payload = {
    "relato_livre": relato_livre,
    "municipio": municipio, "area": area, "estagio": estagio,
    "problema": problema, "solucao": solucao,
    "processo": processo, "gargalo": gargalo, "criterios": criterios,
    "indicador": indicador, "resultado": resultado,
    "papel": papel, "decisor_atual": decisor_atual, "decisor_futuro": decisor_futuro,
    "revisao": revisao, "contrariar": contrariar, "impacto": impacto,
    "pessoais": pessoais, "sensiveis": sensiveis, "origem_dados": origem_dados,
    "fornecedor": fornecedor, "dados_fora": dados_fora,
    "hipotese": hipotese, "escopo": escopo, "indicador_teste": indicador_teste,
    "parada": parada, "reversivel": reversivel
}

st.divider()
if st.button("Analisar caso", type="primary", use_container_width=True):
    st.session_state.result = evaluate(payload)
    st.session_state.meeting_guide = None

if st.session_state.result:
    r = st.session_state.result

    st.header("3. Leitura do Copiloto")
    c1, c2, c3 = st.columns(3)
    c1.metric("Estágio declarado", estagio or "Não informado")
    c2.metric("Estágio sugerido", r["suggested"])
    c3.metric("Prioridade de atenção", r["attention"])
    st.info(r["main"])

    st.subheader("Situação das quatro evidências")
    cols = st.columns(4)
    for i, (name, (status, motive)) in enumerate(r["evidence"].items()):
        with cols[i]:
            st.markdown(f"**{name}**")
            st.markdown(status)
            st.caption(motive)

    left, right = st.columns(2)
    with left:
        st.subheader("O que já sabemos")
        for x in r["known"]:
            st.write("•", x)
        st.subheader("O que ainda precisamos saber")
        for x in r["gaps"]:
            st.write("•", x)

    with right:
        st.subheader("Alertas")
        for x in r["alerts"]:
            st.write("•", x)
        st.subheader("Atores a envolver")
        for x in r["actors"]:
            st.write("•", x)

    st.header("4. Plano para a próxima facilitação")
    p = facilitation_plan(payload, r)

    st.markdown(f"**Objetivo:** {p['objetivo']}")
    st.markdown(f"**Próximo movimento:** {p['movimento']}")
    st.markdown(f"**Entregável esperado:** {p['entregavel']}")

    # ------------------------------------------------------------
    # CAMADA GENERATIVA
    # ------------------------------------------------------------
    st.subheader("✨ Perguntas geradas para a próxima reunião")
    st.caption(
        "A IA usa o relato livre, as lacunas encontradas e o estágio sugerido para formular "
        "perguntas contextuais. Ela não altera a classificação determinística do caso."
    )

    if st.button("Gerar roteiro de reunião com IA", use_container_width=True):
        if not relato_livre.strip():
            st.error("Inclua primeiro um relato livre do facilitador.")
        elif not api_key:
            st.error(
                "Configure uma Gemini API key na barra lateral ou em `.streamlit/secrets.toml`."
            )
        else:
            with st.spinner("Formulando perguntas a partir do relato e das lacunas do caso..."):
                try:
                    guide = generate_meeting_guide(
                        api_key=api_key,
                        model_name=model_name,
                        narrative=relato_livre,
                        structured_case=payload,
                        deterministic_result=r,
                        fallback_plan=p,
                    )
                    st.session_state.meeting_guide = guide
                except GenerativeLayerError as exc:
                    st.error(str(exc))

    if st.session_state.meeting_guide:
        g = st.session_state.meeting_guide

        st.markdown(f"**Objetivo sugerido para a reunião:** {g.meeting_objective}")
        st.markdown(f"**Pergunta de abertura:** {g.opening_question}")

        for item in g.questions:
            with st.expander(f"{item.theme} — {item.question}", expanded=True):
                st.caption(f"Por que perguntar: {item.why_it_matters}")

        st.markdown("**Decisão que a conversa deve permitir:**")
        st.success(g.closing_decision)

        if g.facilitator_caution:
            st.markdown("**Cuidado para o facilitador:**")
            st.warning(g.facilitator_caution)

    else:
        st.markdown("**Roteiro-base sem IA:**")
        for q in p["perguntas"]:
            st.write("•", q)

    st.subheader("Decisão que a próxima etapa deve permitir")
    st.success(p["decisao"])

    st.caption(
        "O Copiloto não substitui a decisão administrativa ou técnica do município. "
        "Regras críticas permanecem explícitas; a camada generativa apoia a preparação da conversa."
    )
