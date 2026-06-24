import { Client, Events, GatewayIntentBits } from 'discord.js';
import * as toml from 'smol-toml';
import * as fs from 'fs';

const _settingRawString = fs.readFileSync("config.toml", { encoding: 'utf8' });
const settings = toml.parse(_settingRawString) as Record<string, any>;

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
    // Ignore messages from bots or messages that do not start with the prefix
    if (message.author.bot || !message.content.startsWith(PREFIX)) return;

    // Split the message into the command and arguments array
    const args = message.content.slice(PREFIX.length).trim().split(/ +/);
    const commandName = args.shift()!.toLowerCase();

    // Command Handling
    if (commandName === 'ping') {
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
