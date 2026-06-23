import streamlit as st
import requests


def fetch_official_joke():
    """Fetch a random joke from the Official Joke API.
    Endpoint: https://official-joke-api.appspot.com/random_joke
    Returns JSON like: {"id":..., "type":"...", "setup":"...", "punchline":"..."}
    """
    url = "https://official-joke-api.appspot.com/random_joke"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return resp.json()


def fetch_icanhazdadjoke():
    """Fetch a random joke from icanhazdadjoke.com (requires Accept: application/json)."""
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json", "User-Agent": "blackjack-advisor-joke-app/1.0"}
    resp = requests.get(url, headers=headers, timeout=5)
    resp.raise_for_status()
    return resp.json()


def get_joke(source: str):
    try:
        if source == "Official Joke API":
            data = fetch_official_joke()
            return data.get("setup"), data.get("punchline"), data
        else:
            data = fetch_icanhazdadjoke()
            # icanhaz returns {"id":..., "joke":"..."}
            return data.get("joke"), None, data
    except requests.RequestException as e:
        # Bubble up network/HTTP errors
        st.error(f"Network error: {e}")
        return None, None, None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None, None, None


def main():
    st.set_page_config(page_title="Random Joke Generator", page_icon="🤖")
    st.title("Random Joke Generator")
    st.write("Click the button to fetch a fresh joke from a public jokes API.")

    source = st.selectbox("Joke source", ["Official Joke API", "icanhazdadjoke.com"])

    if st.button("Get Joke"):
        with st.spinner("Fetching a joke..."):
            setup, punchline, raw = get_joke(source)

        if setup:
            st.subheader("Joke")
            st.write(setup)
            if punchline:
                st.markdown(f"**{punchline}**")

            with st.expander("Show raw JSON response"):
                st.json(raw)
        else:
            st.info("No joke to display. Try again or choose a different source.")

    st.sidebar.markdown("---")
    st.sidebar.markdown("Built with Streamlit and public joke APIs")
    st.sidebar.markdown("Run locally: `streamlit run jokes_app.py`")


if __name__ == "__main__":
    main()
