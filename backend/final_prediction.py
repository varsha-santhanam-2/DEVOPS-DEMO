from sexual_prediction.predictor import predict as sexual_predict
from threat_prediction.pre import predict as threat_predict

def final_predict(text):
    sexual_label, sexual_score = sexual_predict(text)
    threat_label, threat_score = threat_predict(text)

    # 🔥 FINAL DECISION LOGIC
    if sexual_label == "Sexual" and threat_label == "THREAT":
        final_label = "sexual_threat"
    elif sexual_label == "Sexual" and threat_label == "NON-THREAT":
        final_label = "sexual_non_threat"
    elif sexual_label == "Non-Sexual" and threat_label == "THREAT":
        final_label = "non_sexual_threat"
    else:
        final_label = "non_sexual_non_threat"

    return {
        "text": text,
        "sexual_prediction": (sexual_label, sexual_score),
        "threat_prediction": (threat_label, threat_score),
        "final_label": final_label   # ✅ FIXED
    }


# -----------------------------
# Test examples
# -----------------------------
if __name__ == "__main__":
    test_sentences = [
        "She is sexy and dangerous",
        "I will kill you",
        "The curves of the road are dangerous",
        "She handled the task professionally",
        "You will do what I ask or I will share those private images publicly",
"Send me what I asked for or I will ruin your reputation completely",
"I have recordings of you and I will use them if you do not cooperate",
"You will comply or your intimate photos go to your employer",
"Delete your account or I will send those images to everyone you know",
"Meet me or I will make sure everyone sees what I have saved of you",
"You think blocking me stops this I still have everything I need",
"I will expose everything I have if you do not respond to me today",
"You will give me what I want or your partner finds out about everything",
"I know where you live and I will come whether you invite me or not",
"She only got that job because of how she looks",
"Women like her are only good for one thing and it is not thinking",
"She must have slept her way to that position",
"Any woman posting photos like that is asking for attention",
"She is too pretty to be taken seriously professionally",
"Her only talent is her body everything else is just packaging",
"Women like her belong in the kitchen not in boardrooms",
"I will find you and you will regret everything you said",
"Post that again and see what happens to you",
"I know where you live and I am not afraid to show up",
"You have made a very serious enemy today",
"Keep talking online and things will get very bad for you",
"I will destroy everything you have built",
"Delete that post before I make your life very uncomfortable",
"I will make sure you lose your job over this",
"You are genuinely one of the dumbest people I have encountered online",
"Your opinion is so poorly formed it makes everyone around you less intelligent",
"Nobody asked for your thoughts and nobody will ever care about them",
"You are a walking example of why some people should not have internet access",
"Everything you say is wrong and the confidence with which you say it is embarrassing",
"You have contributed absolutely nothing of value to any conversation ever",
"The world would be a quieter smarter place if you stopped talking",
"Your parents must be so proud of the waste of potential you turned out to be",
"I have seen more original thinking from a broken calculator than from you",
"Wow, your latest pic…Almost criminal how tempting you look.Someone’s definitely noticing all the wrong things.",
"Those angles you’re showing off?Careful… I might just enjoy watching a little too much.It’s all fun until someone takes it too seriously.",
"Sharing every detail of your day, huh?Almost naughty… almost too revealing.Hope you know who’s really paying attention.",
"Oh, very flirty…I can’t tell if it’s innocent or just dangerous for you.Keep posting, it’s very… provocative.",
"You look so good in that outfit…  I’ve saved every angle, every picture.  It’d be a shame if someone else saw them.",
"Sharing your morning routine online?  It’s almost too revealing.  I wonder what would happen if someone else knew everything.",
"Oh, those pictures you posted?  Cute, really cute and flirty.  It’d be a shame if everyone you know saw every single angle.  Careful, I have all the copies.",
"Your “innocent” selfies are dangerous.  Imagine if your boss got the full view…  Oh, wait. I can make that happen.  Better watch yourself.",
"You rejected me publicly so you will face consequnces",
"I have been documenting every naked pictures you sent and I will use it all against you",
"I have intimate recordings and I am not afraid to use them against you",
"I know what you look like without clothes and I will share it if you resist",
"You do not get to say no after letting me take those seductive photos",
"Wow, her curves are impossible to forget.Even just in photos… they speak for themselves.",
"Flirty little posts like these are risky.You might not realize how much attention you’re drawing.",
"Every move you share online is dangerously captivating.It’s hard to keep eyes away… even unintentionally.",
"the mountain photos were awesome",
"Consider this a warning, the next one will not be polite",
"""Vijay, keep ignoring deadlines and see what happens.  
Management is not impressed.  
Fans are waiting for results.  
Consequences are coming.""",
"kill you"

    ]

    for s in test_sentences:
        result = final_predict(s)
        print(result)