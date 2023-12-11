import pandas as pd
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

def determine_features(client: OpenAI, title: str, description: str) -> dict:
    response = client.chat.completions.create(
          model = "gpt-3.5-turbo",
          temperature = 1,
          messages = [
              {
                  "role": "user",
                  "content": r'''
                    I have a dataset with two columns, title and description. Based on these two informations, I can determine the features.
                    For example, if the title is: FYY Leather Case with Mirror for Samsung Galaxy S8 Plus, Leather Wallet Flip Folio Case with Mirror and Wrist Strap for Samsung Galaxy S8 Plus Black.
                    And the description is: Premium PU Leather Top quality. Made with Premium PU Leather. Receiver design. Accurate cut-out for receiver. Convenient to Answer the phone without open the case. Hand strap makes it easy to carry around. RFID Technique: Radio Frequency Identification technology, through radio signals to identify specific targets and to read and copy electronic data. Most Credit Cards, Debit Cards, ID Cards are set-in the RFID chip, the RFID reader can easily read the cards information within 10 feet(about 3m) without touching them. This case is designed to protect your cards information from stealing with blocking material of RFID shielding technology. 100% Handmade. Perfect craftsmanship and reinforced stitching make it even more durable. Sleek, practical, and elegant with a variety of dashing colors. Multiple Functions Card slots are designed for you to put your photo, debit card, credit card, or ID card while on the go. Unique design. Cosmetic Mirror inside made for your makeup and beauty. Perfect Viewing Angle. Kickstand function is convenient for movie-watching or video-chatting. Space amplification, convenient to unlock. Kickstand function is convenient for movie-watching or video-chatting.
                    the features will be: {
                        "category": "Phone Accessories",
                        "material": "Premium PU Leather",
                        "features": {
                          "receiver_design": "Accurate cut-out for receiver. Convenient to Answer the phone without opening the case.",
                          "hand_strap": "Yes",
                          "RFID_technique": "Protection of card information with RFID shielding technology",
                          "handmade": "100% Handmade",
                          "stitching": "Reinforced stitching",
                          "functions": {
                            "card_slots": "Yes",
                            "cosmetic_mirror": "Yes",
                            "kickstand_function": "Yes, convenient for movie-watching or video-chatting",
                            "space_amplification": "Yes, convenient to unlock"
                          },
                          "color_options": "Variety of dashing colors",
                          "compatibility": "Samsung Galaxy S8 Plus"
                        }
                    }
                  '''
              },
              {
                  "role": "user",
                  "content": rf'''
                    Based on that, what will be the features of a column with the title {title} and description {description}.
                    Answer me using a JSON format, using just the keys category, meterial and features. Also, don't use any text other than the json.
                    As a last resort, if you don't know a specific value, just leave it as null. But please try your best.
                    '''
              }
          ]
      )
    return json.loads(response.choices[0].message.content)


if __name__ == '__main__':

    load_dotenv()

    client = OpenAI(
        api_key = os.getenv("OPEN_AI_API_KEY"),
        organization = os.getenv("OPEN_AI_ORGANIZATION_KEY")
    )

    product_search_scopus = pd.read_csv(r"tb__c9p336__product_search_scopus_stream_2023-12-09T13_51_18.66683Z.csv")

    for index, row in product_search_scopus.iterrows():
        for key, value in determine_features(client = client, title = row['Title'], description = row['Text']).items():
            if key not in product_search_scopus.columns:
                product_search_scopus[key] = None
            product_search_scopus.at[index, key] = str(value)

    product_search_scopus.to_csv("result.csv", index = False)






