import streamlit as st
from textstat import textstat
from keybert import KeyBERT

# Initialize KeyBERT with a suitable model
kw_model = KeyBERT(model='all-MiniLM-L6-v2')

def calculate_readability_metrics(text):
    return {
        "Flesch Reading Ease": textstat.flesch_reading_ease(text),
        "Flesch-Kincaid Grade Level": textstat.flesch_kincaid_grade(text),
        "Gunning Fog": textstat.gunning_fog(text),
        "SMOG Index": textstat.smog_index(text),
        "Automated Readability Index": textstat.automated_readability_index(text)
    }

def generate_tooltip(metric, score):
    tooltips = {
        "Flesch Reading Ease": "90-100: Very easy, 60-70: Plain English, 0-30: Very difficult",
        "Flesch-Kincaid Grade Level": f"{score}: Suitable for grade {int(score)} students",
        "Gunning Fog": f"{score}: Suitable for grade {int(score)} students",
        "SMOG Index": f"{score}: Years of education needed to understand the text",
        "Automated Readability Index": f"{score}: Corresponds to a U.S. grade level"
    }
    additional_info = {
        "Flesch Reading Ease": "Higher scores indicate material that is easier to read; lower scores indicate more complex material.",
        "Flesch-Kincaid Grade Level": "Lower grades (5-6) are typically clearer for wider audiences.",
        "Gunning Fog": "Lower scores indicate clearer text. Aim for 7-8 for broad accessibility.",
        "SMOG Index": "Lower scores are better for wider accessibility.",
        "Automated Readability Index": "Similar to FKGL but considers characters rather than syllables."
    }
    return f"{tooltips[metric]} - {additional_info[metric]}"

def extract_keywords(text):
    return kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 3), stop_words='english')

def basic_text_metrics(text):
    words = text.split()
    num_words = len(words)
    num_sentences = text.count('.') + text.count('!') + text.count('?')
    average_word_length = sum(len(word) for word in words) / num_words if num_words > 0 else 0
    return num_words, num_sentences, average_word_length

def clarity_and_precision_index(text):
    sentences = text.split('.')
    long_sentences = [sentence for sentence in sentences if len(sentence.split()) > 20]
    long_sentence_percentage = len(long_sentences) / len(sentences) * 100
    feedback = f"{len(long_sentences)} out of {len(sentences)} sentences are too long. "
    feedback += f"This is {long_sentence_percentage:.2f}% of the text. Consider simplifying or splitting long sentences."
    return feedback

def engagement_and_persuasiveness_score(text):
    persuasive_words = {
        'achieve', 'improve', 'success', 'lead', 'benefit', 'gain', 'increase', 'advance',
        'innovate', 'optimize', 'develop', 'drive', 'enhance', 'execute', 'outperform',
        'transform', 'exceed', 'pioneer', 'succeed'
    }
    persuasive_count = sum(1 for word in text.split() if word.lower() in persuasive_words)
    persuasive_word_percentage = persuasive_count / len(text.split()) * 100
    feedback = f"{persuasive_count} persuasive words used, making up {persuasive_word_percentage:.2f}% of the text. "
    feedback += "Consider using more persuasive language to enhance engagement."
    return feedback

# Custom CSS for tooltips
tooltip_css = """
<style>
.tooltip {
  position: relative;
  display: inline-block;
}
.tooltip .tooltiptext {
  visibility: hidden;
  width: 280px;
  background-color: #555;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;
  position: absolute;
  z-index: 1;
  bottom: 150%;
  left: 50%;
  margin-left: -140px;
  opacity: 0;
  transition: opacity 0.3s;
}
.tooltip .tooltiptext::after {
  content: "";
  position: absolute;
  top: 100%;
  left: 50%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: #555 transparent transparent transparent;
}
.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}
</style>
"""

# Streamlit interface setup
st.title("SEO and Readability Analyzer")
st.markdown(tooltip_css, unsafe_allow_html=True)
user_text = st.text_area("Paste your text here:", height=300)

if st.button("Analyze Text"):
    if user_text:
        readability_scores = calculate_readability_metrics(user_text)
        st.write("### Readability Scores")
        for metric, score in readability_scores.items():
            tooltip_text = generate_tooltip(metric, score)
            st.markdown(f'<div class="tooltip">{metric}: {score}<span class="tooltiptext">{tooltip_text}</span></div>', unsafe_allow_html=True)

        keywords = extract_keywords(user_text)
        st.write("### Keywords")
        for keyword, score in keywords:
            st.write(f"{keyword} (Score: {score:.4f})")

        num_words, num_sentences, avg_word_length = basic_text_metrics(user_text)
        st.write("### Basic Text Metrics")
        st.write(f"Word Count: {num_words}, Sentence Count: {num_sentences}, Average Word Length: {avg_word_length:.2f} characters")

        clarity_index = clarity_and_precision_index(user_text)
        st.write("### Clarity and Precision Index")
        st.write(clarity_index)

        engagement_score = engagement_and_persuasiveness_score(user_text)
        st.write("### Engagement and Persuasiveness Score")
        st.write(engagement_score)
    else:
        st.write("Please paste some text to analyze.")
