import { callBackend } from '../core/callBackend.js';
import { Client, Events, Message, TextChannel } from 'discord.js';
import { settings } from '../core/getSettings.js';

export class PingPongCommand {
    prefix: string;

    constructor(client: Client) {
        this.prefix = settings.Discord.Command.Prefix;
        client.on(Events.MessageCreate, (m: any) => this.onMessage(m));
    }

    async onMessage(message: Message<boolean> & {channel: TextChannel}) {
        if (message.author.bot || !message.content.startsWith(this.prefix)) return;
        const args = message.content.slice(this.prefix.length).trim().split(/ +/);
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
        //else if (commandName === 'say') {
        //    // Joins the rest of the arguments array back together into a single string
        //    const textToSay = args.join(' '); 
        //    if (!textToSay) return message.reply('Please provide text for me to repeat!');
        //    await message.channel.send(textToSay);;
        //}
    }
}
