import altair as alt
import pandas as pd


def altair_scatter_plot(df: pd.DataFrame) -> alt.vegalite.v4.api.Chart:

    base_options = list(df['artist_name'].unique())
    base_options.sort()
    options = [None] + base_options
    options_labels = ['All artists'] + base_options
    input_dropdown = alt.binding_select(options=options,
                                        labels=options_labels,
                                        name=' ')

    selector = alt.selection_single(empty='all', fields=['artist_name'])
    dropdown = alt.selection_single(fields=['artist_name'],
                                    bind=input_dropdown)
    scaler = alt.selection_interval(bind='scales')

    scatter = alt.Chart(df)\
                 .mark_circle(size=150,
                              smooth=True,
                              color="#1DB954",
                              stroke='#1f1e1e',
                              strokeWidth=1)\
                 .encode(alt.X('duration_min',
                               title='Duration (Min)'),
                         alt.Y('popularity',
                               title='Popularity',
                               scale=alt.Scale(domain=[0, 100])),
                         opacity=alt.condition(dropdown & selector,
                                               alt.value(1),
                                               alt.value(0.05)),
                         tooltip=[alt.Tooltip('track_name', title='Track'),
                                  alt.Tooltip('artist_name', title='Artist'),
                                  alt.Tooltip('duration_min', title='Duration (min)'),
                                  alt.Tooltip('popularity', title='Popularity')])\
                 .properties(height=350,
                             width=500)\
                 .configure_axis(titleFontSize=16,
                                 labelFontSize=13,
                                 labelFont='Helvetica')\
                 .configure_title(font='Helvetica')\
                 .add_selection(dropdown,
                                scaler,
                                selector)

    return scatter
