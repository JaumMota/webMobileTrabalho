export class Habito {
  constructor(
    public id: number,
    public nome: string,
    public descricao: string,
    public data: Date | null, 
    public feito: boolean
  ) {}
}