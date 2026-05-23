servicos = [
    "Escova",
    "Progressiva",
    "Selagem" ,
    "Botox Capilar"
    "Cronograma Capilar" ,
    "Hidratação",
    "Manicure",
    "Pedicure"
    "Design de Sobrancelhas" ,
    "Micropigmentação de sobrancelhas e labial" ,
    "Maquiagem" ,
    "Limpeza de pele" ,
    "Microagulhamento facial" ,
    "Intradermo terapia capilar",
    "Botox" ,
    "Preenchimento labial" ,
    "Enzimas" ,
    "PEIM(remoção de micro vasos)" ,
    "Drenagem linfática" ,
    
]

def listar_servicos():

    print("\n===== SERVIÇOS DO ESPAÇO JOSY MIRANDA ESTÉTICA =====\n")

    for i, servico in enumerate(servicos, start=1):

        print(f"[{i}] {servico}")

    print("\n==============================")