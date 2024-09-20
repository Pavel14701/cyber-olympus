document.getElementById('connectButton').addEventListener('click', async () => {
    const { Connection, clusterApiUrl, Keypair } = solanaWeb3;
    // Установите соединение с Solana
    const connection = new Connection(clusterApiUrl('devnet'), 'confirmed');
    // Создайте новый ключевой набор
    const keypair = Keypair.generate();
    console.log('Public Key:', keypair.publicKey.toString());
    // Получите баланс аккаунта
    const balance = await connection.getBalance(keypair.publicKey);
    console.log('Balance:', balance);
});