import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { Router } from '@angular/router';
import { CapacitorHttp, HttpOptions } from '@capacitor/core';

@Component({
  standalone: true,
  selector: 'app-adicionar-habito',
  templateUrl: './adicionar-habito.page.html',
  styleUrls: ['./adicionar-habito.page.scss'],
  imports: [
    ReactiveFormsModule, // Necessário para usar FormControlName
    IonicModule, // Necessário para os componentes Ionic
    CommonModule // Necessário para usar diretivas comuns do Angular
  ]
})
export class AdicionarHabitoPage implements OnInit {
  public habitoForm!: FormGroup; 

  constructor(
    private fb: FormBuilder,
    private router: Router
  ) {}

  ngOnInit() {
    // Inicializa o FormGroup
    this.habitoForm = this.fb.group({
      nome: ['', Validators.required],
      descricao: ['', Validators.required]
    });
  }

  adicionarHabito() {
    if (this.habitoForm.invalid) {
      console.log('Preencha todos os campos!');
      return;
    }

    const novoHabito = this.habitoForm.value;

    const options: HttpOptions = {
      url: 'http://127.0.0.1:8000/api/habitos/criar/', 
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${localStorage.getItem('token')}`
      },
      data: novoHabito
    };

    CapacitorHttp.post(options)
      .then((response) => {
        if (response.status === 201) {
          console.log('Hábito adicionado com sucesso:', response.data);
          this.router.navigate(['/habito']); // Redireciona para a página de hábitos
        } else {
          console.error('Erro ao adicionar hábito:', response.status);
        }
      })
      .catch((error) => {
        console.error('Erro ao adicionar hábito:', error);
      });
  }

  cancelarCriacao() {
    this.router.navigate(['/habito']); // Redireciona para a página de hábitos
  }
}