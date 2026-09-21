from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# ============================================
# 1. STATE
# ============================================

class GraphState(TypedDict):
    question: str
    question_type: str
    response: str


# ============================================
# 2. ROUTER NODE
# ============================================

def classify_question(state: GraphState):

    question = state["question"].lower()

    print("\n🔎 Classifying question...")
    print(f"Question: {state['question']}")

    company_keywords = [
        "tcs",
        "infosys",
        "capgemini",
        "accenture"
    ]

    is_company_question = any(
        company in question
        for company in company_keywords
    )

    if is_company_question:
        question_type = "company"
    else:
        question_type = "general"

    print(f"📌 Question Type: {question_type}")

    return {
        "question_type": question_type
    }


# ============================================
# 3. GENERAL NODE
# ============================================

def general_node(state: GraphState):

    print("\n🤖 General Question Node")

    return {
        "response": (
            "This question will be answered "
            "using general knowledge."
        )
    }


# ============================================
# 4. COMPANY NODE
# ============================================

def company_node(state: GraphState):

    print("\n🏢 Company Question Node")

    return {
        "response": (
            "This question will be answered "
            "using the company RAG knowledge base."
        )
    }


# ============================================
# 5. ROUTING FUNCTION
# ============================================

def route_question(state: GraphState):

    if state["question_type"] == "company":
        return "company"

    return "general"


# ============================================
# 6. CREATE GRAPH
# ============================================

graph_builder = StateGraph(GraphState)


# ============================================
# 7. ADD NODES
# ============================================

graph_builder.add_node(
    "classifier",
    classify_question
)

graph_builder.add_node(
    "general",
    general_node
)

graph_builder.add_node(
    "company",
    company_node
)


# ============================================
# 8. START → CLASSIFIER
# ============================================

graph_builder.add_edge(
    START,
    "classifier"
)


# ============================================
# 9. CONDITIONAL EDGE
# ============================================

graph_builder.add_conditional_edges(
    "classifier",
    route_question,
    {
        "general": "general",
        "company": "company"
    }
)


# ============================================
# 10. NODES → END
# ============================================

graph_builder.add_edge(
    "general",
    END
)

graph_builder.add_edge(
    "company",
    END
)


# ============================================
# 11. COMPILE
# ============================================

graph = graph_builder.compile()


# ============================================
# 12. TEST QUESTION
# ============================================

initial_state = {
    "question": "What is the eligibility criteria for TCS?",
    "question_type": "",
    "response": ""
}


# ============================================
# 13. RUN GRAPH
# ============================================

result = graph.invoke(initial_state)


# ============================================
# 14. FINAL RESULT
# ============================================

print("\n" + "=" * 60)
print("FINAL STATE")
print("=" * 60)

print(result)