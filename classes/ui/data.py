import streamlit as st
import pandas as pd
import plotly.express as px


class PlotData:
    """Classe para geração de gráficos no Plotly com validação automática."""

    @staticmethod
    def _prepare_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
        """Normaliza colunas e garante DataFrame seguro."""
        if dataframe is None or dataframe.empty:
            return pd.DataFrame()
        df = dataframe.copy()
        df.columns = [str(col).strip() for col in df.columns]
        return df

    @staticmethod
    def _validate_dataframe(df: pd.DataFrame, required_cols: list) -> bool:
        """Verifica se DataFrame possui colunas obrigatórias e dados."""
        if df.empty:
            st.warning("⚠️ O DataFrame está vazio. Não é possível gerar o gráfico.")
            return False

        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            st.error(
                f"❌ Colunas ausentes: {missing}. "
                f"Colunas disponíveis: {list(df.columns)}"
            )
            return False

        return True

    @classmethod
    def bar_plot(cls, dataframe: pd.DataFrame, x: str, y: str,
                 color: str = "lightblue", title: str = "", show: bool = False):
        """Gera um gráfico de barras."""
        df = cls._prepare_dataframe(dataframe)
        x, y = x.strip(), y.strip()

        if not cls._validate_dataframe(df, [x, y]):
            return None

        fig = px.bar(
            data_frame=df,
            x=x,
            y=y,
            color_discrete_sequence=[color],
            title=title
        )

        if show:
            st.plotly_chart(fig, use_container_width=True)
        return fig

    @classmethod
    def area_plot(cls, dataframe: pd.DataFrame, x: str, y: str,
                  color_name: str, show: bool = False):
        """Gera um gráfico de área no Streamlit."""
        df = cls._prepare_dataframe(dataframe)
        x, y, color_name = x.strip(), y.strip(), color_name.strip()

        if not cls._validate_dataframe(df, [x, y, color_name]):
            return None

        if df[x].dtype == object:
            df[x] = df[x].astype(str).str.strip()
        df[y] = pd.to_numeric(df[y], errors='coerce').fillna(0)

        fig = px.area(df, x=x, y=y, color=color_name)

        if show:
            st.plotly_chart(fig, use_container_width=True)

        return fig

    @classmethod
    def pie_plot(cls, dataframe: pd.DataFrame, names: str, values: str = None,
                 color: str = None, title: str = "", show: bool = False):
        """Gera um gráfico de pizza."""
        df = cls._prepare_dataframe(dataframe)
        names = names.strip()
        value_list = [names]
        if values:
            values = values.strip()
            value_list.append(values)

        if not cls._validate_dataframe(df, value_list):
            return None

        fig = px.pie(df, names=names, values=values, color=color, title=title)

        if show:
            st.plotly_chart(fig, use_container_width=True)

        return fig

    @classmethod
    def line_plot(cls, dataframe: pd.DataFrame, x, y: str,
                  color: str = None, title: str = "", show: bool = False):
        """Gera um gráfico de linha."""
        df = cls._prepare_dataframe(dataframe)
        y = y.strip()
        required_cols = [y]
        if color:
            color = color.strip()
            required_cols.append(color)

        if isinstance(x, str):
            x = x.strip()
            required_cols.append(x)
            if not cls._validate_dataframe(df, required_cols):
                return None
            if df[x].dtype == object:
                df[x] = df[x].astype(str).str.strip()
        else:
            df = df.copy()
            temp_col = "_temp_x"
            df[temp_col] = x
            x = temp_col

        df[y] = pd.to_numeric(df[y], errors='coerce').fillna(0)
        fig = px.line(df, x=x, y=y, color=color, title=title)

        if show:
            st.plotly_chart(fig, use_container_width=True)

        if "_temp_x" in df.columns:
            df.drop(columns=["_temp_x"], inplace=True)

        return fig

    @classmethod
    def scatter_plot(cls, dataframe: pd.DataFrame, x: str, y: str,
                     color: str = None, title: str = "", show: bool = False):
        """Gera um gráfico de dispersão (scatter plot) no Streamlit."""
        df = cls._prepare_dataframe(dataframe)
        x, y = x.strip(), y.strip()
        required_cols = [x, y]
        if color:
            color = color.strip()
            required_cols.append(color)

        if not cls._validate_dataframe(df, required_cols):
            return None

        fig = px.scatter(df, x=x, y=y, color=color, title=title)

        if show:
            st.plotly_chart(fig, use_container_width=True)

        return fig
