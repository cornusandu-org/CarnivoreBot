import { Client, Events, GatewayIntentBits } from 'discord.js';
import { settings } from './core/getSettings.js';
import { callBackend } from './core/callBackend.js';

const client = new Client({ intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
] });

const PREFIX = ':';

client.once(Events.ClientReady, (readyClient) => {
	console.log(`Ready! Logged in as ${readyClient.user.tag}`);
});

client.on(Events.MessageCreate, async message => {
    if (message.author.bot || !message.content.startsWith(PREFIX)) return;

    const args = message.content.slice(PREFIX.length).trim().split(/ +/);
    const commandName = args.shift()!.toLowerCase();

    if (commandName === 'ping') {
        const ratelimit: any = await callBackend('/api/userRatelimits/pingPong', 'GET', { 'userId': message.author.id });
        if (ratelimit.timeLeft > 0) {
            console.error(`PING RATELIMIT REACHED`);
            return;
        }
        await callBackend('/api/userRatelimits/pingPong', 'POST', { 'userId': message.author.id });
        await callBackend('/api/userRatelimits/pingPong', 'REFRESH', {});
        await message.channel.send('Pong!');
    } 
    
    else if (commandName === 'say') {
        // Joins the rest of the arguments array back together into a single string
        const textToSay = args.join(' '); 
        if (!textToSay) return message.reply('Please provide text for me to repeat!');
        
        await message.channel.send(textToSay);
    }
});

client.login(settings?.Discord?.App?.Auth?.AuthToken as string | undefined);
