# Create a function that Recommends top 20 products
from IPython import get_ipython
import joblib
import pickle as pkl
import pandas as pd
import os

review_df = pd.read_csv('sample30.csv')



def recommend_top5_products(user_name):

    # Check if COLAB or Local
    if 'google.colab' in str(get_ipython()):
        In_Colab = True
        user_user_recommendation = pkl.load(open('/content/drive/MyDrive/Recommendation System Project/Pickle/user_user_recommendation_model.pkl','rb')) 
        review_data_sentiment = pkl.load(open('/content/drive/MyDrive/Recommendation System Project/Pickle/review_data_sentiment.pkl','rb'))
        sentiment_model = pkl.load(open('/content/drive/MyDrive/Recommendation System Project/Pickle/xgb_model.pkl','rb'))

        
    else:
        In_Colab = False
        user_user_recommendation = pkl.load(open('Pickle/user_user_recommendation_model.pkl','rb')) 
        review_data_sentiment = pkl.load(open('Pickle/review_data_sentiment.pkl','rb'))
        sentiment_model = pkl.load(open('Pickle/xgb_model.pkl','rb'))
   
    # Check if the user_name is present in the user_user_recommendation
    if user_name not in user_user_recommendation.index:
        return 'User not present in the database'
    
    # Filter top 20 unique products for the user_name
    
    user_user_recommendation = pd.DataFrame(user_user_recommendation.loc[user_name].sort_values(ascending=False)[0:20])
 
   # Get the name and review_vectors from review_data_sentiment  for each product present in user_user_recommendation 
    user_user_recommendation = user_user_recommendation.reset_index()
    user_user_recommendation.columns = ['id', 'rating']



    # Get top 20 products data frame
    top20_products_df = review_data_sentiment[review_data_sentiment.id.isin(user_user_recommendation.id.tolist())]
    top20_products_df = top20_products_df.drop_duplicates(subset=['id'])
    top20_products_df = top20_products_df[['id', 'review_vectors']]




    # Use the sentiment_model to predict the sentiment of the review text
    top20_products_df['sentiment_predicted'] = sentiment_model.predict(top20_products_df['review_vectors'].to_list())

    # Return the top 20 products data frame where the sentiment is positive
    top20_products_df = top20_products_df[top20_products_df['sentiment_predicted'] == 1]



    # For each id in top20_products_df check the percentage of positive sentiment in review_data_sentiment
    top20_products_df['positive_sentiment_percentage'] = top20_products_df['id'].apply(lambda x: review_data_sentiment[review_data_sentiment['id'] == x]['user_sentiment'].mean())


    # Sort the top20_products_df based on the positive_sentiment_percentage and return top 5 products
    top_5_products = top20_products_df.sort_values(by='positive_sentiment_percentage', ascending=False).head(5)

    # Now merge this data with the review_df to get the product name
    top_5_products = pd.merge(top_5_products, review_df[['id', 'name']], left_on='id', right_on='id', how='left')
    top_5_products.drop_duplicates(subset=['id'], inplace=True)

    return list(top_5_products['name'])


recommend_top5_products('aaron')
