import discord
import html
from discord.channel import VoiceChannel
from discord.player import FFmpegPCMAudio
from google.cloud import texttospeech

TOKEN = 'MzYyOTE4NjU5ODg0MDU2NTc2.WczYVw.ZF4HaSbcwPMJdfumeA-V29cUcGw'
client = discord.Client()

voiceChannel: VoiceChannel

@client.event
async def on_ready():
    print('Login!!!')
    await client.change_presence(activity=discord.Game(name="VALORANT", type=3))
    

@client.event
async def on_member_join(member):
    print(member + "さん")


@client.event
async def on_message(message):
    global voiceChannel

    if message.author.bot:
        return
    if message.content == '!morio':
        voiceChannel = await VoiceChannel.connect(message.author.voice.channel)
        await message.channel.send('もりおだよ')
        return
    elif message.content == '!bye':
        voiceChannel.stop()
        await message.channel.send('ばいばい')
        await voiceChannel.disconnect()
        return

    play_voice(message.content)
    

def text_to_ssml(text):
    ecaped_lines = html.escape(text)
    ssml = "{}".format(
        ecaped_lines.replace("\n", '\n<break time="1s"/>')
    )
    return ssml


def ssml_to_speech(ssml, file, language_code, gender):
    ttsClient = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=ssml)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code, ssml_gender=gender
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = ttsClient.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(file, "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file " + file)
    return file


def play_voice(text):

    if "http" in text:
        return
    elif len(text) > 100:
        return

    result_text = text.replace("w", "わら")
    result_text = result_text.replace("ｗ", "わら")
    ssml = text_to_ssml(result_text)
    file = ssml_to_speech(ssml, "voice.mp3", "ja-JP", texttospeech.SsmlVoiceGender.MALE)
    voiceChannel.play(FFmpegPCMAudio(file))

token = getenv('DISCORD_BOT_TOKEN')
client.run(token)
