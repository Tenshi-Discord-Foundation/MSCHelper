from datetime import timedelta

import joblib
import numpy as np
import requests
from disnake.ext import commands

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity


class AntiScam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.model_path = "./src/cogs/scam_model.pkl"
        self.vectorizer_path = "./src/cogs/vectorizer.pkl"

        try:
            self.classifier = joblib.load(self.model_path)
            self.vectorizer = joblib.load(self.vectorizer_path)
            print("[INFO] Model and vectorizer loaded.")

        except FileNotFoundError:
            print("[INFO] Model not found, starting training...")

            self.X_train = [
                "Congrats, you won a million! Click the link to claim your prize!",
                "Free Nitro",
                "Free Steam Gift Card",
                "Free $10 Steam gift",
                "Hurry! Claim your free gift right now!",
                "Exclusive offer! Get a bonus for free.",
                "Free steam gift - https://steamcomm1nity.com/",
                "Claim your steam gift now: https://steamcomm1nity.ru",
                "Free Steam gift card: https://steamcomm1nity.net/gift",
                "You've been selected! Claim your prize now!",
                "Free Nitro gift",
                "Free nitro for Discord",
                "Free TG premium",
                "Claim your free steamcommmnity gift now!",
                "Click the link to get your gift - https://descord-example.com",
                "Free steam Gift Card 20$!!!",
                "New year free gift https://steamcommmnity.ru/promo",
                "Get free VIP access right now!",
                "Freebie! Claim your reward: https://nitroexample.org",
                "Congrats, you won! Click here fast -> http://free-nitro.ru",
                "Hey, how's it going?",
                "Great weather today!",
                "Let's talk about the new game.",
                "Who's at the meeting today?",
                "Interesting article about tech.",
                "Glad to see you in the chat!",
                "Thanks for the help!",
                "Have a good day!",
                "Good luck everyone!",
                "See you soon!",
                "How did you like the last movie?",
                "I need to do my homework.",
                "Who's going to the movies today?",
                "Happy to discuss any questions.",
                "Gonna go walk the dog.",
                "Watched a cool video on YouTube.",
                "Heard there's a server update tomorrow.",
                "How's the project coming along?",
                "Welcome new members!",
                "Great job, keep it up!",
                "Check out this video on YouTube: https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "Here's a link to my steam, rate it - https://steamcommunity/id/777/",
                "when I wrote the word FREE",
                "FREE Ukraina 🇺🇦",
                "FREE",
                "free urine 🇮🇨",
            ]
            self.y_train = [1] * 20 + [0] * 22

            self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
            X_train_vect = self.vectorizer.fit_transform(self.X_train)

            self.classifier = LogisticRegression()
            self.classifier.fit(X_train_vect, self.y_train)

            joblib.dump(self.classifier, self.model_path)
            joblib.dump(self.vectorizer, self.vectorizer_path)

            print("[INFO] Model and vectorizer trained and saved successfully.")

        self.WEBHOOK_URL = "https://discord.com/api/webhooks/1345383651860414525/aMcxpyc1uRDRTLS1Tv5TL1lStO_MJY0805egXdA1-Y2ghFTRNev_DJeO3SSfKxA3QXAq"

    def send_webhook_notification(self, message):
        data = {"content": message}
        requests.post(self.WEBHOOK_URL, json=data)

    def is_suspicious_link(self, text):
        suspicious_domains = [
            "descord",
            "steamcommmnity",
            "nitroexample",
            "free-nitro",
            "tg premium",
        ]
        return any(domain in text.lower() for domain in suspicious_domains)

    def is_scam_ml(self, message_text):
        vect = self.vectorizer.transform([message_text])
        prob = self.classifier.predict_proba(vect)[0][1]
        return prob > 0.5

    def is_similar(self, message_text, previous_messages):
        if not previous_messages:
            return False
        messages = list(previous_messages) + [message_text]
        vects = self.vectorizer.transform(messages)
        sims = cosine_similarity(vects[-1], vects[:-1])
        return np.any(sims > 0.8)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        content = message.content

        if self.is_suspicious_link(content):
            await message.delete()
            msg = await message.channel.send(
                f"{message.author.mention}, that link looks sketchy AF. We don't do that here."
            )
            await msg.delete(delay=5)
            self.send_webhook_notification(
                f"Suspicious link from {message.author.mention}: {content}"
            )
            await message.author.timeout(
                duration=timedelta(minutes=10), reason="Shady link, my dude."
            )
            return

        if self.is_scam_ml(content):
            await message.delete()
            msg = await message.channel.send(
                f"{message.author.mention}, quit trying to scam, my dude. Not cool."
            )
            await msg.delete(delay=5)
            self.send_webhook_notification(
                f"Scam message from {message.author.mention}: {content}"
            )
            await message.author.timeout(
                duration=timedelta(minutes=10), reason="Scam message, my dude."
            )
            return


def setup(bot):
    bot.add_cog(AntiScam(bot))
    print("[INFO] AntiScam loaded")