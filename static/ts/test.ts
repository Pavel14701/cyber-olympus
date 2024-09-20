// Интерфейс для описания структуры данных пользователя
interface User {
    id: number;
    name: string;
    email: string;
}

class UserService {
    private users: User[] = [];

    addUser(user: User): void {
        this.users.push(user);
    }

    // Асинхронный метод для получения пользователя по ID
    async getUserById(id: number): Promise<User | undefined> {
        return new Promise((resolve) => {
            setTimeout(() => {
                const user = this.users.find(user => user.id === id);
                resolve(user);
            }, 1000); // Симуляция задержки в 1 секунду
        });
    }

    // Метод для получения всех пользователей
    getAllUsers(): User[] {
        return this.users;
    }
}

// Пример использования класса UserService

new UserService().addUser({ id: 1, name: 'John Doe', email: 'john.doe@example.com' });
new UserService().addUser({ id: 2, name: 'Jane Smith', email: 'jane.smith@example.com' });

new UserService().getUserById(1).then(user => {
    if (user) {
        console.log(`User found: ${user.name} (${user.email})`);
    } else {
        console.log('User not found');
    }
});

console.log('All users:', new UserService().getAllUsers());
