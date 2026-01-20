from __future__ import annotations

import streamlit as st


def apply_base_styles() -> None:
    st.markdown(
        """
        <style>
        .slide-container {
            padding: 1rem 1.5rem;
            background: linear-gradient(135deg, rgba(248,250,252,0.9), rgba(240,244,248,0.9));
            border-radius: 16px;
            border: 1px solid rgba(148, 163, 184, 0.3);
            animation: fadeIn 0.6s ease-in;
        }
        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(8px);}
            to {opacity: 1; transform: translateY(0);}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
