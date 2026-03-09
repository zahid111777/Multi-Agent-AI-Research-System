"""
Multi-Agent AI Research System - Backend
=========================================
Agents  : Research → Writer → Fact-Checker → Reviewer
Workflow: Topic → Research Notes → Draft → Verified Draft → Final Article
Tech    : LangGraph + OpenAI GPT-4o-mini
"""

import os
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

# ── Environment 
PROJECT_ROOT = Path(__file__).parent.parent.parent
load_dotenv(PROJECT_ROOT / "keys" / ".env")

# ── LLM 
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


# ── State Schema 
class ResearchState(TypedDict):
    topic: str
    research_notes: str
    draft: str
    fact_check_report: str
    final_article: str
    current_step: str


# ── Agent 1 – Research 
def research_agent(state: ResearchState) -> ResearchState:
    """
    Gathers comprehensive research notes for the given topic.
    """
    topic = state["topic"]

    messages = [
        SystemMessage(content=(
            "You are an expert research analyst with deep knowledge across all domains. "
            "Your task is to conduct thorough research on the given topic. "
            "Provide well-structured research notes that include:\n"
            "  • Key facts and statistics\n"
            "  • Important concepts and definitions\n"
            "  • Multiple perspectives and viewpoints\n"
            "  • Recent developments or trends\n"
            "  • Notable examples or case studies\n"
            "Be comprehensive, accurate, and cite logical reasoning for each point."
        )),
        HumanMessage(content=f"Conduct thorough research on the following topic:\n\n**{topic}**"),
    ]

    response = llm.invoke(messages)
    return {
        **state,
        "research_notes": response.content,
        "current_step": "research_complete",
    }


# ── Agent 2 – Writer 
def writer_agent(state: ResearchState) -> ResearchState:
    """
    Writes a well-structured article draft from the research notes.
    """
    topic = state["topic"]
    research_notes = state["research_notes"]

    messages = [
        SystemMessage(content=(
            "You are an expert journalist and content writer. "
            "Using the provided research notes, write a compelling, well-structured article. "
            "The article must include:\n"
            "  • An engaging introduction that hooks the reader\n"
            "  • Clearly organized sections with descriptive markdown headers (##)\n"
            "  • Smooth transitions between sections\n"
            "  • Supporting evidence drawn from the research notes\n"
            "  • A strong conclusion that summarizes key insights\n"
            "Write in a professional yet accessible tone. Target length: 600–900 words."
        )),
        HumanMessage(content=(
            f"Topic: **{topic}**\n\n"
            f"Research Notes:\n{research_notes}\n\n"
            "Write a complete article draft based on these research notes."
        )),
    ]

    response = llm.invoke(messages)
    return {
        **state,
        "draft": response.content,
        "current_step": "draft_complete",
    }


# ── Agent 3 – Fact-Checker 
def fact_checker_agent(state: ResearchState) -> ResearchState:
    """
    Reviews the draft against the research notes and produces a fact-check report.
    """
    draft = state["draft"]
    research_notes = state["research_notes"]

    messages = [
        SystemMessage(content=(
            "You are a meticulous fact-checker and editorial critic. "
            "Your job is to rigorously cross-reference an article draft against the source research notes. "
            "In your report:\n"
            "  • List claims in the draft that are NOT supported by the research notes\n"
            "  • Flag any logical inconsistencies or unsupported assumptions\n"
            "  • Highlight statements that are vague and need more precision\n"
            "  • Note any missing important information from the research that should be in the article\n"
            "  • List items that ARE accurate and well-supported (Verified Facts)\n"
            "Format your report with clear sections: "
            "**Issues Found**, **Suggested Corrections**, and **Verified Facts**."
        )),
        HumanMessage(content=(
            f"Article Draft:\n{draft}\n\n"
            f"Original Research Notes:\n{research_notes}\n\n"
            "Produce a comprehensive fact-check report."
        )),
    ]

    response = llm.invoke(messages)
    return {
        **state,
        "fact_check_report": response.content,
        "current_step": "fact_check_complete",
    }


# ── Agent 4 – Reviewer 
def reviewer_agent(state: ResearchState) -> ResearchState:
    """
    Produces the final, publication-ready article by applying the fact-check corrections.
    """
    topic = state["topic"]
    draft = state["draft"]
    fact_check_report = state["fact_check_report"]

    messages = [
        SystemMessage(content=(
            "You are a senior editorial reviewer and polishing expert. "
            "Your task is to produce a final, publication-ready article by:\n"
            "  • Incorporating ALL corrections from the fact-check report\n"
            "  • Improving clarity, flow, and readability\n"
            "  • Strengthening the introduction and conclusion\n"
            "  • Ensuring consistent tone and style throughout\n"
            "  • Removing any redundancy or awkward phrasing\n"
            "Output ONLY the final polished article — no commentary or meta-text."
        )),
        HumanMessage(content=(
            f"Topic: **{topic}**\n\n"
            f"Draft Article:\n{draft}\n\n"
            f"Fact-Check Report:\n{fact_check_report}\n\n"
            "Produce the final polished article."
        )),
    ]

    response = llm.invoke(messages)
    return {
        **state,
        "final_article": response.content,
        "current_step": "review_complete",
    }


# ── Build LangGraph 
def build_graph() -> StateGraph:
    workflow = StateGraph(ResearchState)

    # Register nodes
    workflow.add_node("research", research_agent)
    workflow.add_node("writer", writer_agent)
    workflow.add_node("fact_checker", fact_checker_agent)
    workflow.add_node("reviewer", reviewer_agent)

    # Define the linear pipeline
    workflow.set_entry_point("research")
    workflow.add_edge("research", "writer")
    workflow.add_edge("writer", "fact_checker")
    workflow.add_edge("fact_checker", "reviewer")
    workflow.add_edge("reviewer", END)

    return workflow.compile()


# Compiled graph (importable by frontend)
graph = build_graph()


# ── Utility: run full pipeline 
def run_pipeline(topic: str) -> ResearchState:
    """
    Runs the full research pipeline synchronously and returns the final state.
    """
    initial_state: ResearchState = {
        "topic": topic,
        "research_notes": "",
        "draft": "",
        "fact_check_report": "",
        "final_article": "",
        "current_step": "starting",
    }
    return graph.invoke(initial_state)


# ── Utility: stream pipeline step-by-step 
def stream_pipeline(topic: str):
    """
    Yields (node_name, state) tuples as each agent completes.
    Useful for real-time UI updates.
    """
    initial_state: ResearchState = {
        "topic": topic,
        "research_notes": "",
        "draft": "",
        "fact_check_report": "",
        "final_article": "",
        "current_step": "starting",
    }
    for step in graph.stream(initial_state):
        for node_name, node_state in step.items():
            yield node_name, node_state


# ── CLI quick-test 
if __name__ == "__main__":
    import sys

    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "The impact of AI on software development"
    print(f"\n{'='*60}")
    print(f"  Multi-Agent AI Research System")
    print(f"  Topic: {topic}")
    print(f"{'='*60}\n")

    for node, state in stream_pipeline(topic):
        label = {
            "research":     "Research Agent",
            "writer":       "Writer Agent",
            "fact_checker": "Fact-Checker Agent",
            "reviewer":     "Reviewer Agent",
        }.get(node, node)
        print(f"✅ {label} completed.\n")

    result = run_pipeline(topic)
    print("\n" + "="*60)
    print("FINAL ARTICLE")
    print("="*60)
    print(result["final_article"])
