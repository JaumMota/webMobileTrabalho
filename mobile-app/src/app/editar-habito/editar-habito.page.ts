import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { ActivatedRoute, Router } from '@angular/router';
import { CapacitorHttp, HttpOptions } from '@capacitor/core';
import { Storage } from '@ionic/storage-angular'; // Importação do Storage

@Component({
  standalone: true,
  selector: 'app-editar-habito',
  templateUrl: './editar-habito.page.html',
  styleUrls: ['./editar-habito.page.scss'],
  imports: [
    CommonModule, // Necessário para diretivas comuns do Angular
    ReactiveFormsModule, // Necessário para usar FormControlName
    IonicModule // Necessário para os componentes Ionic
  ]
})
export class EditarHabitoPage implements OnInit {
  public habitoForm!: FormGroup;
  public id!: number;

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private storage: Storage // Adicionado para recuperar o token
  ) {}

  async ngOnInit() {
    await this.storage.create(); // Garante que o Storage está pronto
    this.id = Number(this.route.snapshot.paramMap.get('id'));

    this.habitoForm = this.fb.group({
      nome: ['', Validators.required],
      descricao: ['', Validators.required]
    });

    this.carregarHabito();
  }

  async salvarEdicao() {
    if (this.habitoForm.invalid) {
      console.log('Preencha todos os campos!');
      return;
    }

    const usuario = await this.storage.get('usuario'); // Recupera o usuário do Storage
    const token = usuario?.token;

    if (!token) {
      console.error('Token não encontrado. Faça login novamente.');
      return;
    }

    const dadosAtualizados = this.habitoForm.value;

    const options: HttpOptions = {
      method: 'PUT', // Método HTTP explícito
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${token}` // Usa o token recuperado do Storage
      },
      url: `http://127.0.0.1:8000/api/habitos/${this.id}/editar/`,
      data: dadosAtualizados
    };

    console.log('Usuário recuperado:', usuario); // Log para verificar o usuário
    console.log('Enviando requisição de edição:', options); // Log para verificar os dados da requisição

    CapacitorHttp.put(options)
      .then((response) => {
        if (response.status === 200) {
          console.log('Hábito editado com sucesso:', response.data);
          this.router.navigate(['/habito']); // Redireciona para a lista de hábitos
        } else {
          console.error('Erro ao editar hábito:', response.status);
        }
      })
      .catch((error) => {
        console.error('Erro ao editar hábito:', error);
      });
  }

  carregarHabito() {
    // Simulação: substitua por uma chamada ao backend para obter os dados do hábito
    const habito = { nome: 'Hábito Atual', descricao: 'Descrição Atual' }; // Exemplo
    this.habitoForm.patchValue(habito);
  }
}
