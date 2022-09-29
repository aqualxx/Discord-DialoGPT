import discord
import random
import asyncio

from .ai import ChatAI
from .args import get_arguments

class ChatBot(discord.Client):
    """Main discord class to listen to messages and respond if conditions are met"""
    async def on_ready(self):
        self.bot = ChatAI()
        self.arguments = get_arguments()
        self.doneMessaging = True

        print('Logged in as '+self.user.name+' (ID:'+str(self.user.id)+') | Connected to '+str(len(self.guilds))+' servers')
        print('--------')
        print("Discord.py verison: " + discord.__version__)
        print('--------')

    async def on_message(self, message):
        # Don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.strip() == "":
            return
        
        # do we have permission to talk in the channel?
        if self.get_effective_permissions(message.channel).send_messages == False:
            return

        mentioned = False
        always_reply_id = []
        if not self.arguments.whitelist == 0:
            always_reply_id.append(self.arguments.whitelist)
        
        # if whitelisted, uses the custom response chance instead of 100%
        whitelisted = False
        whitelisted_id = []

        # Have we been mentioned in the message?
        if self.user.mentioned_in(message):
            mentioned = True

        # Are we in a channel that does not need a prefix?
        for id in always_reply_id:
            if message.channel.id == id:
                mentioned = True

        # Are we in a channel that is whitelisted?
        for id in whitelisted_id:
            if message.channel.id == id:
                whitelisted = True

        # if the channel is not whitelisted or mentioned, don't respond
        if not whitelisted and not mentioned:
            return

        # If we weren't pinged and we get unlucky, don't respond
        if random.random() > self.arguments.response_chance and not mentioned:
            return

        await self.send_message(message)

    async def send_message(self, message):
        """Filter message and ask bot for to send a response"""
        # Don't respond if we are still messaging
        if self.doneMessaging == False:
            # Use new ephemeral feature
            await message.reply("Messaging another person!", ephemeral=True)
            return

        self.doneMessaging = False

        print("Got message '{0.content}' from '{0.author}'!".format(message))

        processed_message = self.filter_message(message.content)

        # Simulate the bot typing
        async with message.channel.typing():
            res = self.bot.generate_response(processed_message, self.arguments)
            await asyncio.sleep(max(random.random(), 0.5))
            
        print("Replying to {0.author}".format(message)+" with '"+res+"'")

        self.doneMessaging = True

        if self.arguments.reply == 1:
            await message.reply(res, mention_author=False)
            return
        
        await message.channel.send(res)
        

    def filter_message(self, message):
        """Filter out message"""
        # Filter out user id and username
        message.replace("@"+self.user.name+"#"+self.user.discriminator, "")
        message.replace("@"+self.user.name, "")

        return message

    def get_effective_permissions(self, channel):   
        """Get permissions that we have in a specific channel id"""  
        me = channel.guild.me

        granted_perms = me.guild_permissions

        role_list = [me] + me.roles

        for role in role_list:
            ovr = channel.overwrites_for(role)
            allow, deny = ovr.pair()

            granted_perms.value = granted_perms.value & (~deny.value)

            granted_perms.value = granted_perms.value | allow.value

        return granted_perms