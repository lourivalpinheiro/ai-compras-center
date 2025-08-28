import streamlit as st
from typing import Union

class DisplayMetrics:
    """Classe para exibir métricas no Streamlit com delta e ajuda."""

    def __init__(
        self,
        name: str,
        value: Union[int, float, str],
        delta: Union[int, float, str] = None,
        help: str = None,
        delta_color: str = "normal"
    ):
        """
        Exibe uma métrica no Streamlit.

        :param name: Nome/label da métrica.
        :param value: Valor da métrica (int, float ou str).
        :param delta: Variação da métrica (delta) opcional.
        :param help: Texto de ajuda/tooltip.
        :param delta_color: Cor do delta (normal, inverse, off).
        """
        st.metric(
            label=name,
            value=value,
            delta=delta,
            delta_color=delta_color,
            help=help
        )
