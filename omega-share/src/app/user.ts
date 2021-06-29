export class User {
    
    constructor(
        public id: number,
        public userName: string,
        public role: string,
        public email?: string,
        public about?: string,
        public firstName?: string,
        public lastName?: string,
        

    ) {  }
}