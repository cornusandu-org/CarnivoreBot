import { Client, Events, GatewayIntentBits } from 'discord.js';
import { settings } from './core/getSettings.js';
import { PingPongCommand } from './feat/pingPong.js';

const client = new Client({ intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
] });

client.once(Events.ClientReady, (readyClient) => {
	console.log(`Ready! Logged in as ${readyClient.user.tag}`);
});

const features = [
    new PingPongCommand(client)
];


client.login(settings?.Discord?.App?.Auth?.AuthToken as string | undefined);
