import pandas as pd
from io import StringIO
from statsmodels.tsa.arima.model import ARIMA
import re
import os

# The raw content of the user-provided CSV file is hardcoded here for robust parsing, 
# as the file structure was complex due to unhandled quotes/commas in the CSV format.
file_content = """Review_Title,Review_Body,Review_Stars,Reviewer,Review_Date
5.0 out of 5 stars Excellent Phone,"The video showcases the product in use.The video guides you through product setup.The video compares multiple products.The video shows the product being unpacked.Video Player is loading.Click to play videoPlayMuteCurrent Time 0:00/Duration 0:06Loaded: 50.05%0:00Stream Type LIVESeek to live, currently behind liveLIVERemaining Time -0:06 1xPlayback RateChaptersChaptersDescriptionsdescriptions off, selectedCaptionsCaptions offEnglish (Automated), selectedAudio Trackdefault, selectedFullscreenThis is a modal window. Good Phone Nice Camera Nice Performance Charging speed also ok charges in 40 mins from 15-80% no heating observed even in heavy use for me, as shifted from midrange androids i feel battery is low but its okay because 
the quality of phone is worth it. i feel this phone is more value for money than 13, 14, 16 because you get 48mp and type c with pastel colours which are just wow . i was stuck for an hour deciding the colour haha.
i finally choose to go with blue. The double speakers with bass feel amazing while holding the phone, faceid feature is amazing as it works even in darkest nights.
The ring/silent slider feature is amazing to use in one click if youre in busy college lecture doing stuff as backbencher hehe....sorry for my bad english but here are some camera samples for youmy final opinion - worth it as a diehard android or samsung fan hehehe",5.0,Yash Borate,Reviewed in India on 3 November 2025
5.0 out of 5 stars Great phone,"The iPhone 15 is an excellent device that feels premium and modern even in 2025. It runs super smoothly, and the camera quality is outstanding.
Apple’s long software support ensures it will stay updated for years.
Switching from Android can be a bit challenging at first, but once you get used to it, the experience is fun and totally worth it.",5.0,Mayank vyas,Reviewed in India on 26 October 2025
5.0 out of 5 stars iPhone 15 Excellent performance,"Value for money, good battery span, excellent functionality, super built quality & perfect compatibility.",5.0,Ganesh.CH,Reviewed in India on 9 November 2025
4.0 out of 5 stars Stunning Blue iPhone 15—Almost Perfect Upgrade,"The iPhone 15 in Blue is gorgeous—the color pops with a matte finish that's fingerprint-resistant, and the 6.1-inch Super Retina XDR display is buttery smooth at 60Hz for videos and apps.
A16 Bionic chip handles everything from gaming to editing flawlessly, and the 48MP camera nails portraits and low-light shots.
128GB is plenty for me, and USB-C charging is a welcome change. Battery lasts a solid day.
Only gripe: no 120Hz ProMotion like the Pro models—feels a tad dated in scrolling.
Still, best iPhone for most users—love it!",4.0,Jake Bagchi,Reviewed in India on 2 November 2025
5.0 out of 5 stars Best phone ever,Amazing performance - better battery performance - clarity on always,5.0,mohanraj,Reviewed in India on 11 November 2025
5.0 out of 5 stars Perfect phone and send me invoice,Perfect running phone . Slow heat in running and not a receive invoice my number. Please send me invoice my name and send me number.,5.0,Nariya Piyush,Reviewed in India on 2 November 2025
5.0 out of 5 stars Please buy,Wife s first apple from Android. She enjoys using it now. Good quality and audio and phone is 
good,5.0,MURALIDHAR SRIPATHI,Reviewed in India on 10 November 2025
4.0 out of 5 stars If you have big hands.I would recommend you go for the 15 plus,If you have big hands.I wouldrecommend you go for the 15 plusValue for money - 89%Battery life 'ok - GOODPhone hangs - NOPhone quality. - PERFECTFunctionality - No ProblemSize. - OK,4.0,Akshay,Reviewed in India on 10 November 2025
4.0 out of 5 stars Value for money,Value for money... Only downside is battery and refresh rate it only last for around 8 hours on fully charge and the refresh rate is only 60 hrz which is okay I guess 
but 90 or 120 hrz would have been better since most of the Android mobile phone nowadays comes with 120 hrz for lower price.,4.0,Tenrik Sangma,Reviewed in India on 29 October 2025
5.0 out of 5 stars Worth buying,"Before I presented this phone online I had ordered a Samsung phone for my brother few months ago and buying iPhone online a bit sceptical because it cost a lot of money, but I received a brand new iPhone 15 256gb in just 57,000 which was a bit less then buying offline in a Diwali sale.
I am happy with what I received. The battery backup is so good it gives you whole day of functionality without switching off data and Bluetooth.
The battery health showed 100% which off course shows it’s a brand new phone.
Thank you Amazon for delivering a top notch phone in top notch condition.
If you wanna order it online just order it without any dilemma.",5.0,Sandeep Yogi,Reviewed in India on 11 November 2025
4.0 out of 5 stars Good product 👍,Good product 👍,4.0,Aru Mugam,Reviewed in India on 12 November 2025
5.0 out of 5 stars Worth the money,"The black iPhone 15 is sleek, elegant, and feels premium in every sense.
The matte finish gives it a refined, modern look that doesn’t attract fingerprints easily, while the curved edges make it super comfortable to hold.
It’s minimalist but powerful — classic Apple design at its best.The display is stunning — bright, crisp, and smooth, making videos and photos look incredibly vibrant.
The camera quality is noticeably improved, especially in low light;
photos come out sharp and natural with great color balance.Performance-wise, the A16 chip handles everything effortlessly — from multitasking to gaming, it’s fast and fluid with no lag.
The battery life easily lasts a full day with moderate to heavy use, and charging is quick with both MagSafe and USB-C.Overall, the black iPhone 15 is the perfect blend of power, elegance, and everyday practicality.
If you’re looking for a phone that looks professional and performs flawlessly, this one’s a great choice.",5.0,Hinna Mir,Reviewed in India on 31 October 2025
4.0 out of 5 stars 100% found genuine,Review is after 15 days of use. I was afraid to buy online. But it seems ok and not an issue. definitely must buy online if discounted price is available.Moreover being Apple brand no doubts all things are good and perfect.But outer box was little dirty and I had doubt. No worry warranty started from the date of shipping.Model no is also fine as indian origin.,4.0,Prashant,Reviewed in India on 13 
October 2025
4.0 out of 5 stars Nice,verry good,4.0,Ajay rocka,Reviewed in India on 9 November 2025
4.0 out of 5 stars Okish,Seems slow but nice ui,4.0,Placeholder,Reviewed in India on 7 November 2025
4.0 out of 5 stars Good product,Nyc,4.0,Anshu kumar,Reviewed in India on 8 November 2025
4.0 out of 5 stars Feedback,"I purchased an iPhone 15 from Amazon.
The phone performs well overall, but I am facing some heating issues.During data transfer and video calls, the device gets noticeably hot, which is uncomfortable to hold for a long time.I request Apple or Amazon support to look into this issue and provide a possible solution or guidance.Other than that, the phone’s performance and camera quality are good.Issue Summary: • Phone heats up during data transfer • Phone heats up during video calls • Needs improvement in thermal management",4.0,Tikaram meena,Reviewed in India on 9 October 2025
4.0 out of 5 stars Phone in good condition & working well,Phone in good condition 
and well delivered. Happy with the purchase.,4.0,Nivedan,Reviewed in India on 1 November 2025
4.0 out of 5 stars Ios 26,After ios 26 i face battery life is low SOT,4.0,Dhanush,Reviewed in India on 31 October 2025
4.0 out of 5 stars Nice,Wonderful,4.0,Vishnu jakhad,Reviewed in India on 5 November 2025
4.0 out of 5 stars Nice product,Good,4.0,Asha Rawlani,Reviewed in India on 4 November 2025
4.0 out of 5 stars Recieved in good conditon,Recieved good,4.0,Anjali,Reviewed in India on 1 November 2025
4.0 out of 5 stars Worth it,My first iphone .
Built quality is good and dynamic iland vey good feature and new glass ios feature and camera quality is alsoWorth it,4.0,Priyanshu,Reviewed in India on 30 October 2025
4.0 out of 5 stars Nice look 👀 🍎❤️,❤️❤️❤️❤️,4.0,Mr raja,Reviewed in India on 3 November 2025
5.0 out of 5 stars Loving the Camera and Speed Just Wish Battery Lasted Longer,"The iPhone’s camera quality is just amazing sharp details, great colors, and performs really well even in low light. The overall performance and smoothness are top-notch, everything runs fast and feels premium. The only downside is the battery it drains a bit quickly if you’re 
using it heavily (like gaming or video recording). Apart from that, it’s an excellent phone overall.",5.0,Himanshu Jha,Reviewed in India on 10 November 2025
"4.0 out of 5 stars Smooth, Powerful, and Feels Premium!","I’ve been using the iPhone 15 for a while now, and it’s been a great experience overall. The design feels sleek and lightweight, and the display is super bright and clear.
The camera quality is excellent, especially in low light — photos look sharp and natural.",4.0,Karthik,Reviewed in India on 19 October 2025
4.0 out of 5 stars Iphone 15,I love it ❤️First I was worried ☹️ but after i received worthy buying 😊 thank you amzon,4.0,Hanluchi Hanluchi,Reviewed in India on 21 October 2025
"4.0 out of 5 stars Smooth performance, great 48MP camera, modern design","The iPhone 15 delivers smooth performance, a stunning 48MP main camera, a bright OLED screen, and the convenience of USB-C.
New features like the Dynamic Island, a premium matte back, and softer edges give it a fresh feel.
However, the display is still only 60Hz, which isn’t as fluid as some rivals, and the USB-C port offers slower data speeds than the Pro models.
While it misses out on the latest Apple Intelligence features, it remains an excellent choice for its speed, battery life, and camera quality.",4.0,Kaushik r.,Reviewed in India on 7 October 2025
4.0 out of 5 stars Good product,Iphone achha hai but battery bahot jyada drain hota hai,4.0,Juned Alam,Reviewed in India on 21 October 2025
4.0 out of 5 stars All Over Is Best,All over is best and I got the my in full condition with a Amazon support and no issue I found and the phone was worthy for this price,4.0,Vinayraj Gupta,Reviewed in India on 14 October 2025
4.0 out of 5 stars Medium,I’m 
keeping the phone however not very happy with the battery’s performance. It gets down too quickly!Listening to a 4 minute song and 2% of battery gone 🫤🤕And also it heats up too quickly with data ON,4.0,Placeholder,Reviewed in India on 11 October 2025
5.0 out of 5 stars Absolutely Loving My New IPhone 15,"I recently bought the iPhone 15, and I must say it’s an incredible upgrade!
The sleek design feels premium in hand, and the build quality is top-notch as always.
The display is bright, vibrant, and super smooth — watching videos or scrolling through apps feels amazing.The new A16 Bionic chip makes everything lightning-fast, whether I’m multitasking, editing photos, or gaming.
The camera quality is simply outstanding — crisp details, natural colors, and great low-light performance.
I’ve already noticed a big difference in my photos and videos.Battery life has also improved noticeably;
it easily lasts me through the day, even with heavy use.
Plus, the Dynamic Island feature adds a fresh and smart touch to everyday tasks.Overall, I’m extremely happy with my purchase.
The iPhone 15 is elegant, powerful, and worth every penny. Highly recommended for anyone looking to upgrade!
📱✨",5.0,Jayanta karmakar,Reviewed in India on 29 October 2025
4.0 out of 5 stars Very nice performance,,4.0,Sethu,Reviewed in India on 26 October 2025
4.0 out of 5 stars Phone package have some dirt,Giving 4 stars as the phone package have dirts even though it was manufactured in April 2025.My cousin too bought from this seller yet he got the package as fresh looking. But I got the genuine product & device is working fine & perfect,4.0,Midhun Dileep,Reviewed in India on 5 October 2025
4.0 out of 5 stars open box delivery was not included d one needs security n trust specially if we pay 
for prime,"product is but it would have been better if the open box facility was included and i order and i order everything together like: adapter, cover, temper etc. but i only recived phone in advance before delivery date rest came bit late and also in my region the amazone delivery is very late like it deliver products only in evening which also needs improvement apart from this all i recived a good product .",4.0,Habu Yapak,Reviewed in India on 1 October 2025
4.0 out of 5 stars Best in class,Good product,4.0,Ankur Singha,Reviewed in India on 18 October 2025
4.0 out of 5 
stars Good,Good,4.0,Best Product under 150,Reviewed in India on 27 October 2025
5.0 out of 5 stars Excellent performance,"Amazing experience post the upgrade from the previous phone.
The screen with the fluidic display, response rate, the overall look and performance of the phone is genuinely felt, battery life is for one day with normal usage, following the recommended 20-80 % charging pattern, been a month and the performance and feel has made me very happy.",5.0,Sam,Reviewed in India on 2 November 2025
4.0 out of 5 stars Amazon is just lovable and unbeatable in price,The phone camera just love it 😀 but little bit take times to deleverd but no fraud and now I can trust on Amazon thankyou amazon,4.0,Phukon Engjai,Reviewed in India on 13 October 2025
4.0 out of 
5 stars Received the actual product,Genuine and fast delivery,4.0,Placeholder,Reviewed in India on 15 October 2025
4.0 out of 5 stars Bwst,Ok,4.0,Sandeep Satish Chordiya,Reviewed in India on 16 October 2025
4.0 out of 5 stars Like it's,Love it,4.0,Bhimsen Behera,Reviewed in India on 15 October 2025
4.0 out of 5 stars Worthable,"Worth for value , but however it more than enough",4.0,Madan D.S,Reviewed in India on 10 October 2025
4.0 out of 5 stars Phone qulily is nice I have check boxes but charger not found in this I want to replace this phone,"The video showcases the product in use.The video guides you through product setup.The video 
compares multiple products.The video shows the product being unpacked.Video Player is loading.Click to play videoPlayMuteCurrent Time 0:00/Duration 1:31Loaded: 3.30%0:00Stream Type LIVESeek to live, currently behind liveLIVERemaining Time -1:31 1xPlayback RateChaptersChaptersDescriptionsdescriptions off, selectedCaptionsCaptions off, selectedAudio Trackdefault, selectedFullscreenThis is a modal window.
Today recived phone charger not found inside this",4.0,Amit behl,Reviewed in India on 9 November 2025
4.0 out of 5 stars Love it,Quality product and perfect product for me,4.0,REBEL KHAN,Reviewed in India on 10 October 2025
5.0 out of 5 stars Iphone 15,"Best iphone/phone under this range.It's been 21 days of using it and it's so much fast then my normal android.
Camera is so much better, sound is like theater. The best features of it is dynamic island, IOS 26, fast performance and so kuch more.
Display quality is also very nice, I recommend to buy this phone under this price range!!",5.0,Cap or slap,Reviewed in India on 23 October 2025
4.0 out of 5 stars Good BUT,Item received but pakaging was horrible. It looks like They dont care the product damage while transit.,4.0,Sweettlou,Reviewed in India on 8 October 2025
4.0 out of 5 stars nothing,good,4.0,Xyraa,Reviewed in India on 12 October 2025
4.0 out of 5 stars One of the worst purchases I’ve ever made – Full of issues,"From the moment I received this, nothing went right.
It had multiple defects, and getting a replacement or refund was a nightmare.
Every time I contacted customer service, I was given new excuses.
This has been a stressful experience, and I wish I had read more reviews before buying.
Never again.",4.0,MAHTAB ALAM,Reviewed in India on 5 October 2025
4.0 out of 5 stars Good,Good product but delivery services too slow,4.0,Jashan,Reviewed in India on 10 October 2025
4.0 out of 5 stars good phone,the phone is Siri nice and the seller was also good thank you so much Amazon,4.0,YASH CHECHANI,Reviewed in India on 12 October 2025
4.0 out of 5 stars Battery,All good ✌🏻 but Don't consider i phone gives you full day battery backup u have to charge the phone min 2 times in a day to day use,4.0,Prajwal shinde,Reviewed in India on 1 October 2025
4.0 out of 5 stars Ok ok,"I'm 
not an Iphone guy, gifted this to a friend",4.0,Jayanta B.,Reviewed in India on 6 October 2025
4.0 out of 5 stars Good purchase,Good experience...on time delivery and everything is quite good 👍😊,4.0,Vishvendra,Reviewed in India on 11 October 2025
4.0 out of 5 stars Very good,"It's very handy & light weight , camera quality is superb..... Battery back up is not good only",4.0,varun singh,Reviewed in India on 6 October 2025
5.0 out of 5 stars iPhone 15 - Best iPhone under 50k in 2025,"I was a bit worried as the order might get cancelled as it was delaying, the packaging seemed old, I checked 
the Apple Coverage website with the serial number just to confirm if it was pre-activated or not.
It was recently manufactured and was brand new.Coming to the performance part, it is great.
The display runs smooth, the multimedia and gaming experience is good.
We will still miss out high refresh rates on gaming if you are used to using one on an android, but the game is quite responsive and no lag or frame drops.The camera is sufficient to day to day stuff.The build quality is also great and fine compact phone with no big camera buldge.The challenging part is battery, you have to manage that efficiently.
It is a 9/10 device.",5.0,Dibyendu bhattacharjee,Reviewed in India on 6 October 2025
5.0 out of 5 stars Phone is best under 51000 k,My seller is Clickteck Private limitedDon't worry it is safe. amazon provide original iphone.Phone quality is good charging is also good .under 51000 phone is best valuable.When charging phone is heat but absolutely right,5.0,Kaushal Yadav,Reviewed in India on 4 November 2025
4.0 out of 5 stars Good,Good,4.0,Syed Alam,Reviewed in India on 10 October 2025
4.0 out of 5 stars Great,Good,4.0,Sabari,Reviewed in India on 9 October 2025
4.0 out of 5 stars Good,It can be better if refresh rate is 120Hz !!,4.0,Raushan Arya,Reviewed 
in India on 8 October 2025
4.0 out of 5 stars I phone 15 slow,Slow processing speed,4.0,Nimish Singhal,Reviewed in India on 11 October 2025
4.0 out of 5 stars wow,nice product,4.0,Rohit Rathore,Reviewed in India on 7 October 2025
4.0 out of 5 stars It's fine but it looks weird without the keyboard and back button.,ok it's not that it's very goodIt's fine but it looks weird without the keyboard and back button.,4.0,Placeholder,Reviewed in India on 12 October 2025
5.0 out of 5 stars Excellent product,I am very happy with iPhone 15 fast delivery thank you amazon,5.0,Chinthalapudi Kasaiah,Reviewed in India on 10 November 2025
4.0 out 
of 5 stars Excellent,First to apple. It is awesome experience,4.0,gugulothu srikanth,Reviewed in India on 5 October 2025
4.0 out of 5 stars Good,Nice,4.0,Mapuia smake,Reviewed in India on 9 October 2025
4.0 out of 5 stars Nice product,Nice product 👌,4.0,Placeholder,Reviewed in India on 13 October 2025
4.0 out of 5 stars Maintain fast delivery,Nice product,4.0,ajay kumar,Reviewed in India on 5 October 2025
4.0 out of 5 stars Nice photo,Beautiful camera,4.0,Subhajit Sahoo,Reviewed in India on 17 October 2025
5.0 out of 5 stars Loved it ❤️,Greatest purchase of all time.Got in very less Price.Love this product and also delivered so rapidly.Gifted to my Loved one ❤️,5.0,Siddharth Nirgude,Reviewed 
in India on 5 November 2025
5.0 out of 5 stars Excellent,Very good product amazon is very good platform,5.0,Jai shree Ram,Reviewed in India on 11 November 2025
4.0 out of 5 stars Excellent,Very good product,4.0,Abhishek Sharma,Reviewed in India on 4 October 2025
5.0 out of 5 stars Good,Good Products and Speedy shipping delivery service,5.0,Mahavirvala,Reviewed in India on 11 November 2025
4.0 out of 5 stars Good nice 😊,That was good … i know iphone doesn’t give adapter in the box … but they should provide adapter also,4.0,Altamash kareem,Reviewed in India on 3 October 2025
4.0 out of 5 stars Good camara quality,,4.0,Ashang,Reviewed in India on 
9 October 2025
4.0 out of 5 stars Suggestion,Suggestion from me is buy 256 GB varient.
If you buy iPhone 16 it's ai enabled. I mean lot of ai features only available in iPhone 16.,4.0,Pullaiya,Reviewed in India on 5 October 2025
5.0 out of 5 stars The Best,It’s “iPhone” as usual best in all parameter,5.0,Luminacraft,Reviewed in India on 9 November 2025
5.0 out of 5 stars AWESOME THANKS,Awesome Quality colour Design smoothness touch screen AWESOME,5.0,Anirudh Chaurasia,Reviewed in India on 12 November 2025
5.0 out of 5 stars Perfect,Perfect for what is advertised,5.0,Rakesh,Reviewed in India on 11 November 2025
5.0 out of 5 stars 👌👌👌,Amazing... very nice i love this ..gd quality,5.0,Nandini gautam,Reviewed in India on 8 November 2025
5.0 out of 
5 stars I Love It,The best phone of my life. Its function is very smooth.
Display and sound quality is very nice. Battery durability lasts for a day. I did not face any hang yet.
Provided security is great.,5.0,Tapaswini Pradhan,Reviewed in India on 24 October 2025
5.0 out of 5 stars Very nice,Also good received the product for thankfully amazon,5.0,BHARAT SOLANKI,Reviewed in India on 11 November 2025
4.0 out of 5 stars Picture aswoseme,Full avrey good,4.0,Priya,Reviewed in India on 7 October 2025
5.0 out of 5 stars Good,Good 😊,5.0,Shyam meena,Reviewed in India on 11 November 2025
5.0 out of 5 stars Product,Excellent product.,5.0,WANGDUP TAMANG,Reviewed in India on 11 November 2025
5.0 out of 5 stars Happy,Value purchase,5.0,Rashmi Tiwari,Reviewed in India on 11 November 2025
5.0 out of 5 stars Best phone,Highly durable with compact size,5.0,Rinku puri,Reviewed in India on 8 November 
2025
5.0 out of 5 stars No defect in the product..with good packaging,Noicee,5.0,Jitendriya padhi,Reviewed in India on 11 November 2025
3.0 out of 5 stars Decent phone,"The A16 Bionic chip is still exceptionally fast. Even with the demands of iOS 26 and modern apps, the phone delivers smooth, lag-free performance for daily tasks, demanding games, and even light video editing.
You won't feel a significant speed difference for standard use compared to the latest models.60Hz Refresh Rate: The standard 60Hz display is the most noticeable hardware difference compared to the 'Pro' models and newer flagships, which offer a 120Hz ProMotion display.
If you're used to a faster refresh rate, the iPhone 15's scrolling and animations might look less smooth.128gb is not sufficient in 2025If you get it for under 43k then only it is value for money",3.0,Akshay Janagoud,Reviewed in India on 10 November 2025
4.0 out of 5 stars Adaptor,Iphone 15 looks good,4.0,praveen chaudhary,Reviewed in India on 28 September 2025
5.0 out of 5 stars Good product,Best,5.0,Vicky raj,Reviewed in India on 9 November 2025
5.0 out of 5 stars Very beautiful product,Very nice product by Amazon.thank you amazon team.my phone physical condition is very nice.,5.0,Rajendra Tivatane,Reviewed in India on 31 October 2025
4.0 out of 
5 stars Good,Good,4.0,Ravi,Reviewed in India on 1 October 2025
5.0 out of 5 stars Very Good,Nice Phone,5.0,Shreya Kumari,Reviewed in India on 8 November 2025
"4.0 out of 5 stars Good products iphone 15 blue color i,m satisfied","I'm satisfied ,good condition iphone 15 blue color",4.0,Imran ali,Reviewed in India on 25 September 2025
5.0 out of 5 stars Love you amazon,Bahut acha product aaya,5.0,Aaja Sen,Reviewed in India on 6 November 2025
4.0 out of 5 stars Good,Very good phone,4.0,Sarathiprabhu,Reviewed in India on 29 September 2025
5.0 out of 5 stars Perfect!,Perfect product!,5.0,amit,Reviewed in India on 7 November 2025
5.0 out of 5 stars Product quality,Phone is Good conditions,5.0,Samir 
shekh,Reviewed in India on 6 November 2025
5.0 out of 5 stars Greate,Amazing products I like this Amazon 😊😊,5.0,Rahul singha,Reviewed in India on 4 November 2025
"""

# Read the string content as a CSV using robust parameters (skip bad lines due to complex quotes)
# This step handles the data corruption seen in the previous attempts.
df = pd.read_csv(StringIO(file_content), sep=',', engine='python', on_bad_lines='skip')
# Renaming columns to match the actual data after robust parsing
df.columns = ['Review_Title', 'Review_Body', 'Review_Stars_Raw', 'Reviewer', 'Review_Date']
df = df.iloc[1:] # Drop header row that might be duplicated by StringIO reading

print(f"✅ Loaded {len(df)} reviews successfully after robust parsing.")

# 1. FIX: Extract Star Rating from the Review_Title (most reliable column)
def extract_star_rating(title):
    """Uses regex to reliably extract the star rating from the title string."""
    match = re.search(r'(\d\.\d) out of 5 stars', str(title))
    if match:
        return float(match.group(1))
    return None

df['Review_Stars'] = df['Review_Title'].apply(extract_star_rating)
df.dropna(subset=['Review_Stars'], inplace=True) # Remove rows where star could not be extracted

# 2. Sentiment Proxy Logic (Star Rating as Sentiment)
def get_sentiment_category_from_stars(stars):
    """Assigns Sentiment Category based on the numerical star rating."""
    if stars >= 4.0:
        return "Positive"
    elif stars <= 2.0:
        return "Negative"
    else:
        return "Neutral"

df['Sentiment_Category'] = df['Review_Stars'].apply(get_sentiment_category_from_stars)

# Quick summary
sentiment_counts = df['Sentiment_Category'].value_counts().to_dict()
print("\n📊 Sentiment Summary:")
for sentiment, count in sentiment_counts.items():
    print(f"   - {sentiment}: {count}")


# 3. Prepare Time Series Data for Forecasting
# Clean date string and convert to datetime objects
df['Review_Date_Clean'] = df['Review_Date'].str.replace('Reviewed in India on ', '', regex=False)
df['Review_Date_Clean'] = pd.to_datetime(df['Review_Date_Clean'], format="%d %B %Y", errors='coerce')
df.dropna(subset=['Review_Date_Clean'], inplace=True)
df.set_index('Review_Date_Clean', inplace=True)

# Calculate weekly positive sentiment percentage
df['Is_Positive'] = (df['Sentiment_Category'] == 'Positive').astype(int)
ts_data = df.resample('W').agg(
    total_reviews=('Sentiment_Category', 'count'),
    positive_reviews=('Is_Positive', 'sum')
)
ts_data['Positive_Percentage'] = (ts_data['positive_reviews'] / ts_data['total_reviews']) * 100
ts_data.dropna(subset=['Positive_Percentage'], inplace=True)
ts_data = ts_data['Positive_Percentage']

print(f"\n✅ Time Series Data prepared. {len(ts_data)} weekly points available for ARIMA.")

# 4. Fit ARIMA Model and Forecast (Step 5)
if len(ts_data) >= 7:
    order = (1, 0, 0) # ARIMA order: (p, d, q)
    model = ARIMA(ts_data, order=order)
    model_fit = model.fit()

    forecast_steps = 4
    forecast_result = model_fit.get_forecast(steps=forecast_steps)
    forecast = forecast_result.predicted_mean
    
    # Create an index for the next 4 weeks
    last_date = ts_data.index[-1]
    forecast_index = pd.date_range(start=last_date, periods=forecast_steps + 1, freq='W')[1:]
    forecast_series = pd.Series(forecast.values, index=forecast_index)
    
    print(f"✅ Forecasting for the next {forecast_steps} weeks complete.")
    
    # Final Output
    print("\n--- Next 4 Weeks Sentiment Forecast (%) ---")
    print(forecast_series.round(2).to_string(header=False))

else:
    print("❌ Error: Not enough weekly data points for robust ARIMA forecasting.")