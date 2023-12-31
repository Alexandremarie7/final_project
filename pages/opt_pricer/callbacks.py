from dash.dependencies import Input, Output, State
from dash import callback, Output, Input, State
from data.formules_black_scholes import *
from data.stock_data import *
from data.pricer_template import *
from data.risk_free_rates import *
import plotly.graph_objects as go

from server import app

# def get_callbacks (put_pricer):
#     @callback(
#     Output('latest-price', 'children'),
#     Output('put-price', 'children'),
#     Output('layout', 'figure'),
#     Input('put-pricer-button', 'n_clicks'),
#     State('company-choice', 'value'),
#     State('strike-price', 'value'),
#     State('time-selection', 'value'),
#     State('rate-selection', 'value'),
#     State('volatility-selection', 'value')
# )
#     def put_price_producer(n_clicks : int, company, strike_p, time_to_exp, rate, volatility):
#         temp_stock = stocks['Symbol'].loc[stocks["Nom"].str.contains(company)].iat[0]
#         adjusted_time = 30 #A calculer

#         latest_price = stocks_close[temp_stock].iat[len(stocks_close[temp_stock])-1]

#         put_price = put(float(latest_price), float(strike_p), float(rate), 0, adjusted_time, 0)

#         graph_prix = graph_prix_stock (temp_stock, company)

#         return latest_price, put_price, graph_prix




def get_callbacks_pricer ():
    @callback(
        Output('prediction-graph', 'figure'),
        Output('stock-graph', 'figure'),
        Output('risk-free-graph', 'figure'),
        Output('last-price', 'children'),
        Output('nb-days', 'children'),Output('nb-days-v2', 'children'),Output('nb-days-v3', 'children'),Output('nb-days-v4', 'children'),
        Output('variation-last-period', 'children'),
        Output('german-rates-adjusted', 'children'),
        Output('hist-vol-past-days', 'children'),
        Output('hist-vol-5-years', 'children'),
        Output('GARCH-vol', 'children'),
        Output('call-price', 'children'),
        Output('put-price', 'children'),
        Output('graph-call', 'figure'),
        Output('graph-put', 'figure'),

        Input('put-pricer-button', 'n_clicks'),
        State('company-choice', 'value'),
        State('number-period', 'value'),
        State('period-choice', 'value'),
        State('rate-selector-type', 'value'),   
        State('volatility-selector-type', 'value'),
        State('user-rate', 'value'),
        State('user-volatility', 'value'),
        State('strike-price', 'value')
    )
    def option_price_producer(n_clicks : int, company, nb_period, period_type, type_rate, type_vol, user_rate, user_vol, strike_price):

        if period_type == 'Days' :
            nb_days = nb_period
        elif period_type == 'Months' :
            nb_days = nb_period * 22
        elif period_type == 'Years' :
            nb_days = nb_period * 252 #Nb de jours de cotation dans l'année

        
        GARCH_vol = 3 #A modif!!!!!!!!!

        temp_stock = stocks['Symbol'].loc[stocks["Nom"].str.contains(company)].iat[0]

        latest_price = get_stock_latest_price(temp_stock)
        var_last_period = variation_rendering(round(get_stock_return(temp_stock, nb_days),2))

        adjusted_rates =  find_adjusted_rate(nb_days)
        # hist_vol = get_hist_volatility(temp_stock, nb_days)

        hist_vol_past_days = round(get_hist_volatility_given_period(temp_stock, nb_days),2)
        hist_vol_5_years = round(get_hist_volatility(temp_stock, nb_days),2)
        

        graph_prix = graph_prix_stock (temp_stock, company)
        graph_vol_predicted = GARCH_model_vol_prediciton_testing(temp_stock,company)
        graph_risk = graph_yield_curve ()

        if type_rate == 1 : #User's rate
            final_rate = float(user_rate)
        else : #We take the rate provided by the german bonds
            final_rate = float(adjusted_rates)
        
        if type_vol == 1 : #User's vol
            final_vol = user_vol
        elif type_vol == 2 : #We take the historical volatility of the same period of time in the past
            final_vol = hist_vol_past_days
        elif type_vol == 3 : #We take the historical volatility of the past 5 years, adjusted for our number of days
            final_vol = hist_vol_5_years
        else : #We take the volatility predicted by the GARCH model 
            final_vol = GARCH_vol

        call_price = call (latest_price, strike_price, final_rate/100, final_vol/100, nb_days/252)

        
        put_price = put (latest_price, strike_price, final_rate, final_vol, nb_days/252)

        graph_call = graph_call_profit (latest_price, strike_price, call_price, company)
        graph_put = graph_put_profit (latest_price, strike_price, put_price, company)

        return [graph_vol_predicted,
                graph_prix,
                graph_risk, 
                str(round(latest_price,2)) + ' €',
                nb_days,
                nb_days,
                nb_days,
                nb_days,  
                var_last_period,
                adjusted_rates,
                hist_vol_past_days,
                hist_vol_5_years,
                GARCH_vol,
                round(call_price, 2),
                round(put_price,2),
                graph_call,
                graph_put
        ]


# def get_callbacks_pricer (): #put_pricer
#     @callback(
#         Output('prediction-graph', 'figure'),
#         Output('put-price', 'value'),
#         Output('stock-graph', 'figure'),
#         Output('stock-price', 'value'),
#         Output('last-price', 'children'),
#         Output('variation-last-period', 'children'),
#         Output('time-period','children'),
#         Input('put-pricer-button', 'n_clicks'),
#         State('volatility-choice', 'value'),
#         State('company-choice', 'value'),
#         State('strike-price', 'value'),
#         State('date-choice', 'value'),
#         State('rate-selection', 'value'),
#     )
#     def put_price_producer(n_clicks : int, choice_volatility : int, company, strike_p, time_to_exp, rate, volatility):
#         temp_stock = stocks['Symbol'].loc[stocks["Nom"].str.contains(company)].iat[0]
#         adjusted_time = 2 #A calculer

#         latest_price = stocks_data['Close'][temp_stock].iat[len(stocks_data['Close'][temp_stock])-1]
#         put_test = put(latest_price, strike_p, 0.02, 0.04, adjusted_time, 0)

#         graph_prix = graph_prix_stock (temp_stock, company)

#         graph_vol_predicted = GARCH_model_vol_prediciton_testing(temp_stock,company)

#         price_period_before = float(stocks_data['Close'][temp_stock].iat[len(stocks_data['Close'][temp_stock])-adjusted_time-1])
#         var_last_period = variation_rendering(round((((float(latest_price)-price_period_before)/price_period_before)*100),2))

#         if choice_volatility == 1:
#             a=2
#             #action si volatilité du garch
#         elif choice_volatility == 2:
#             a=3
#             #Action volaitlité historique
#         elif choice_volatility == 3:
#             a=4

#         return graph_vol_predicted,  put_test, graph_prix, temp_stock, str(round(latest_price,2)) + ' €', var_last_period, adjusted_time