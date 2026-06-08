import streamlit as st 
from Services.weatherService import WeatherService
from Services.geminiService import GeminiService
from Services.newsService import NewsService


st.set_page_config(
    page_title="Your Morning Buddy",
    page_icon="☀️",
    layout="wide",
)


@st.cache_resource
def load_services():
    return GeminiService(), WeatherService(), NewsService()


gemini_service, weather_service, news_service = load_services()


# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("Navigation")
st.sidebar.divider()

page = st.sidebar.radio(
    "Choose a page:",
    [
        "Home",
        "Get Weather of your City",
        "News by Interest",
        "Smart Planner",
    ],
)

st.sidebar.divider()


# -----------------------------
# Home Page
# -----------------------------
if page == "Home":
    st.title("☀️ Your Morning Buddy")
    st.divider()

    st.header("A Thought for Your Day")

    if "thought" not in st.session_state:
        st.session_state["thought"] = gemini_service.get_thought_for_day()

    st.info(st.session_state["thought"])

    if "motivation_image" not in st.session_state:
        st.session_state["motivation_image"] = gemini_service.get_image_for_thought(
            st.session_state["thought"]
        )

    if st.session_state["motivation_image"]:
        st.image(st.session_state["motivation_image"], use_container_width=True)


# -----------------------------
# Weather Page
# -----------------------------
elif page == "Get Weather of your City":
    st.title("Get Weather of the City")

    city = st.text_input("Enter your city name:")

    if st.button("Fetch Information"):
        if city:
            with st.spinner("Fetching weather information..."):
                st.session_state["weather_data"] = weather_service.get_current_weather(city)
                weather_summary = gemini_service.get_weather_summary(st.session_state["weather_data"])

                st.markdown(f"## {weather_summary}")
                st.success("Weather fetched successfully ✅")
        else:
            st.warning("Please enter a city name.")


# -----------------------------
# News Page
# -----------------------------
elif page == "News by Interest":
    st.title("News by Interest")

    topic = st.text_input("Enter your news interest:")

    if st.button("Fetch News"):
        if topic:
            articles = news_service.get_news_by_topic(topic)
            st.session_state["articles"] = articles
        else:
            st.warning("Please enter a topic.")

    if "articles" in st.session_state:
        st.subheader("Top related articles")
        columns = st.columns(5)

        for index, article in enumerate(st.session_state["articles"][:5]):
            with columns[index]:
                st.subheader(article.get("title", "No title"))
                st.write(f"Source: {article.get('source', 'Unknown')}")
                st.write(article.get("description", "No description available."))
                st.markdown(f"[Read full article]({article.get('url')})")

                if st.button("Quick summary", key=f"summary_{index}"):
                    summary = gemini_service.get_news_summary(article)
                    st.info(summary)

                st.divider()


# -----------------------------
# Smart Planner Page
# -----------------------------
elif page == "Smart Planner":
    
    plan = gemini_service.create_smart_plan(st.session_state["weather_data"])
    st.write(plan)
