import streamlit as st
import pandas as pd
import json
import time

# Charger les QCM depuis un fichier JSON ou CSV
def load_qcm(file):
    try:
        if file.name.endswith('.json'):
            data = json.load(file)
            if "questions" in data:
                return data["questions"]
            else:
                st.error("Le fichier JSON n'est pas valide. Assurez-vous qu'il contient une clé 'questions'.")
                return []
        elif file.name.endswith('.csv'):
            return pd.read_csv(file).to_dict(orient='records')
        else:
            st.error("Format de fichier non supporté. Veuillez utiliser JSON ou CSV.")
            return []
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        return []

# Interface pour jouer au QCM
def play_qcm(qcm_data):
    st.subheader("🌟 Jouer au QCM 🌟")
    if not qcm_data:
        st.warning("Aucun QCM chargé. Veuillez charger un fichier JSON ou CSV.")
        return

    # Initialiser les variables de session pour suivre le score et la progression
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.answers = []
        st.session_state.timer_start_time = time.time()
        st.session_state.question_validated = False  # État pour gérer les validations

    # Obtenir la question actuelle
    current_index = st.session_state.current_question
    if current_index >= len(qcm_data):
        show_results(qcm_data)
        return

    current_qcm = qcm_data[current_index]

    # Afficher la barre de progression
    st.progress((current_index + 1) / len(qcm_data))

    # Afficher la question et les choix
    st.write(f"### Question {current_index + 1} / {len(qcm_data)}")
    st.write(current_qcm["question"])
    selected = st.radio(
        "Choisissez une réponse :",
        options=current_qcm["choices"],
        key=f"choice_{current_index}"
    )

    # Gérer le timer
    elapsed_time = time.time() - st.session_state.timer_start_time
    remaining_time = max(15 - int(elapsed_time), 0)
    timer_placeholder = st.empty()
    timer_placeholder.markdown(f"⏳ Temps restant : {remaining_time} secondes")

    # Bouton pour valider la réponse
    col1, col2 = st.columns([2, 2])
    with col1:
        validate = st.button("Valider", key=f"validate_{current_index}")
    with col2:
        next_question = st.button("Passer à la question suivante", key=f"next_{current_index}")

    # Validation de la réponse
    if validate and not st.session_state.question_validated:
        if selected == current_qcm["correct_answer"]:
            st.success("Bonne réponse ! 🎉")
            st.session_state.score += 1
        else:
            st.error(f"Mauvaise réponse. La bonne réponse était : {current_qcm['correct_answer']}.")

        # Sauvegarder la réponse donnée
        st.session_state.answers.append({
            "question": current_qcm["question"],
            "selected": selected,
            "correct": selected == current_qcm["correct_answer"]
        })
        st.session_state.question_validated = True

    # Passage à la question suivante
    if (next_question or remaining_time == 0) and st.session_state.question_validated:
        st.session_state.current_question += 1
        st.session_state.timer_start_time = time.time()  # Réinitialiser le minuteur
        st.session_state.question_validated = False
    elif next_question and not st.session_state.question_validated:
        st.warning("Veuillez valider votre réponse avant de passer à la question suivante.")

# Résumé des résultats
def show_results(qcm_data):
    st.subheader("🎉 Résultats du QCM 🎉")
    st.write(f"### Score final : {st.session_state.score}/{len(qcm_data)}")
    if st.session_state.score > len(qcm_data) // 2:
        st.balloons()
        st.success("Félicitations mon amour ❤️ ! Tu as réussi haut la main 😘.")
    else:
        st.info("Courage mon cœur, tu feras mieux la prochaine fois 🥰.")

    # Résumé des réponses
    st.write("### Résumé des réponses")
    for i, answer in enumerate(st.session_state.answers):
        st.write(f"**Question {i + 1}** : {answer['question']}")
        st.write(f" - Réponse donnée : {answer['selected']}")
        if answer['correct']:
            st.write(" - ✅ Correcte")
        else:
            st.write(" - ❌ Incorrecte")

    # Réinitialiser l'état pour rejouer
    if st.button("Rejouer le QCM"):
        del st.session_state.current_question
        del st.session_state.score
        del st.session_state.answers
        del st.session_state.timer_start_time
        del st.session_state.question_validated

# Personnalisation de l'interface
def setup_interface():
    st.markdown(
        """
        <style>
        .title {
            font-size: 3em;
            color: #e63946;
            text-align: center;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .heart {
            color: #ff2e63;
            font-size: 1.2em;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="title">Pour toi ma coquine ❤️</div>', unsafe_allow_html=True)

# Ajout de contenu visuel dans la barre latérale
def setup_sidebar():
    st.sidebar.image("image.png", caption="❤️ Toi et moi pour toujours ❤️", use_container_width=True)
    st.sidebar.markdown(
        """
        <div style="text-align: center;">
            <h2 style="color: #e63946;">Menu</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.sidebar.markdown("---")
    nav_option = st.sidebar.radio(
        "Navigation",
        ["📥 Charger QCM", "🎮 Jouer au QCM"],
        key="nav_radio"
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Conseils d'amour 🌹")
    st.sidebar.markdown(
        """
        - Crois en toi et en nous 👫
        - Apprends chaque jour 💡
        - Profite de chaque instant ❤️
        """
    )
    st.sidebar.markdown("---")
    st.sidebar.image("flowers.png", caption="🌸 Juste pour toi 🌸", use_container_width=True)
    return nav_option

# Initialisation
setup_interface()
nav_option = setup_sidebar()

# Variable de session pour les QCM
if "qcm_data" not in st.session_state:
    st.session_state.qcm_data = []

# Gestion de la navigation
if nav_option == "📥 Charger QCM":
    st.subheader("💌 Charger un fichier de QCM")
    uploaded_file = st.file_uploader("Téléchargez un fichier JSON ou CSV contenant vos QCM.", type=["json", "csv"])
    if uploaded_file:
        st.session_state.qcm_data = load_qcm(uploaded_file)
        st.success(f"{len(st.session_state.qcm_data)} questions chargées avec succès !")
elif nav_option == "🎮 Jouer au QCM":
    play_qcm(st.session_state.qcm_data)
