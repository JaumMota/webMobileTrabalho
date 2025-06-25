export class Habito {
  constructor(
    public id: number,
    public nome: string,
    public descricao: string,
    public data: Date | null, // Permite que o campo seja null
    public feito: boolean
  ) {}
}