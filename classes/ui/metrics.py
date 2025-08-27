import streamlit as st
from typing import Union

class DisplayMetrics:
    """Classe para exibir métricas no Streamlit com delta e ícone de ajuda."""

    def __init__(
        self,
        name: str,
        value: Union[int, float, str],
        delta: Union[int, float, str] = None,
        help_icon: str = "",
        border: bool = True,
        delta_color: str = "normal"
    ):
        """
        Exibe uma métrica no Streamlit.

        :param name: Nome/label da métrica.
        :param value: Valor da métrica (int, float ou str).
        :param delta: Variação da métrica (delta) opcional.
        :param help_icon: Texto de ajuda/tooltip.
        :param border: Exibe borda ao redor da métrica.
        :param delta_color: Cor do delta (normal, inverse, off).
        """
        st.metric(
            label=name,
            value=value,
            delta=delta,
            help=help_icon,
            border=border,
            delta_color=delta_color
        )
