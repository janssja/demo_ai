import streamlit as st
import openai
import json

OPENAI_API_KEY = st.secrets["openai_api_key"]
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def app():
    st.title("Een artikel schrijven")

    # Onderwerp Kiezen: Begin met het kiezen van een relevant onderwerp dat je passie wekt en waarvan je denkt dat het waardevol zal zijn voor je lezers. Het moet iets zijn waarover je zowel geïnformeerd als enthousiast bent.
    onderwerp = st.text_area("Waarover gaat je artikel?")
    # Doelpubliek Bepalen: Denk na over wie je wilt bereiken met je artikel. Het begrijpen van je doelpubliek helpt om de toon, stijl en inhoud beter af te stemmen.
    doelgroep = st.text_area("Voor wie is het artikel bedoeld?")
    
    # Vooronderzoek Doen: Verzamel informatie, statistieken, studies of andere relevante bronnen om je artikel te ondersteunen. Dit zorgt voor geloofwaardigheid en diepgang.
    if st.button("Artikel schrijven"):
        with st.spinner("Bezig met zoeken ..."):
            prompt = f"Zoek 7 punten over {onderwerp} voor {doelgroep}."
            st.write(f"Vooronderzoek: {prompt}")
            completion = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                response_format={ "type": "json_object" },
                max_tokens=1000,
                messages=[
                    {"role": "system", "content": """
                        Jij bent een expert in het opzoeken van informatie en zoekt informatie over het gevraagde onderwerp. 
                        Je geeft de antwoorden in een JSON object terug. 
                        Graag alles in de Nederlandse taal.
                    """},
                    {"role": "user", "content": prompt}
                ]
            )
            vooronderzoek = completion.choices[0].message.content

            json_object = json.loads(vooronderzoek)

            # Voor alle lijnen in de JSON van het vooronderzoek diepen we de informatie verder uit
            uitdieping = ""
            for key, value in json_object.items():
                with st.spinner(f"Bezig met het uitdiepen van: {value}"):
                    completion = client.chat.completions.create(
                        model="gpt-4-turbo-preview",
                        max_tokens=1000,
                        messages=[
                            {"role": "system", "content": """
                                Jij bent een expert in het opzoeken van informatie en zoekt informatie over het gevraagde onderwerp. 
                            """},
                            {"role": "user", "content": f"Zoek informatie over {value}"}
                        ]
                    )
                    uitdieping += completion.choices[0].message.content + "\n\n"
            st.write(uitdieping)
        
    # Hoofdpunten Uitwerken: Schrijf een lijst met de belangrijkste punten of ideeën die je in je artikel wilt bespreken. Dit helpt bij het structureren van je gedachten en zorgt ervoor dat je niets belangrijks vergeet.

    # Titel en Inleiding: Schrijf een aantrekkelijke titel en een inleiding die de aandacht trekt. Je inleiding moet het onderwerp introduceren en de lezer prikkelen om verder te lezen.

    # Hoofdgedeelte: Ontwikkel je hoofdpunten in afzonderlijke paragrafen of secties. Zorg ervoor dat elke paragraaf één idee of concept behandelt. Gebruik koppen, subkoppen, bullet points, en afbeeldingen om de tekst te structureren en te verduidelijken.

    # Persoonlijke Touch: Voeg je eigen ervaringen, meningen of persoonlijke verhalen toe om het artikel relatiever en unieker te maken.

    # Conclusie: Rond je artikel af met een sterke conclusie die de belangrijkste punten samenvat en de lezer met iets om over na te denken achterlaat.

    # Revisie en Redactie: Herlees je artikel meerdere keren en maak wijzigingen waar nodig. Let op grammatica, spelling en zinsbouw. Het kan ook nuttig zijn om iemand anders je artikel te laten lezen voor feedback.

    # SEO Optimalisatie: Optimaliseer je artikel voor zoekmachines door relevante trefwoorden op te nemen, maar zorg ervoor dat het natuurlijk blijft en niet geforceerd aanvoelt.

    # Publicatie en Promotie: Publiceer je blogartikel en promoot het via sociale media, e-mailnieuwsbrieven of andere kanalen om het bereik te vergroten.
