import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormGroup, FormBuilder, Validators } from '@angular/forms';
import { IonicModule, ToastController, NavController, LoadingController, AlertController } from '@ionic/angular';
import { Storage } from '@ionic/storage-angular';
import { Usuario } from '../home/usuario.model';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { Habito } from './habito.model';
import { Router } from '@angular/router';

// 👇 Adicionada constante para base URL
const API_BASE_URL = 'http://10.90.8.231:8000';

@Component({
  standalone: true,
  selector: 'app-habito',
  templateUrl: './habito.page.html',
  styleUrls: ['./habito.page.scss'],
  imports: [
    ReactiveFormsModule, // Necessário para usar FormControlName
    FormsModule, // Necessário para usar [(ngModel)]
    IonicModule, // Necessário para os componentes Ionic
    CommonModule // Necessário para usar diretivas comuns do Angular
  ],
  providers: [Storage]
})
export class HabitoPage implements OnInit {
  public usuario: Usuario = new Usuario();
  public lista_habitos: Habito[] = [];
  public exibirFormulario = false;
  public habitoForm!: FormGroup;
  public novoHabito = { nome: '', descricao: '' };
  public instancia = { username: '', password: '' };
  hoje: Date = new Date();

  constructor(
    private fb: FormBuilder,
    public storage: Storage,
    public controle_toast: ToastController,
    public controle_navegacao: NavController,
    public controle_carregamento: LoadingController,
    private alertController: AlertController,
    private router: Router
  ) {}

  async ngOnInit() {
    await this.storage.create();
    const registro = await this.storage.get('usuario');

    if (registro) {
      this.usuario = Object.assign(new Usuario(), registro);
      this.consultarHabitosSistemaWeb();
    } else {
      this.controle_navegacao.navigateRoot('/home');
    }

    // Inicializa o FormGroup
    this.habitoForm = this.fb.group({
      nome: ['', Validators.required],
      descricao: ['', Validators.required]
    });
  }

  // ✅ Adicionado para atualizar a lista ao retornar para a página
  ionViewWillEnter() {
    if (this.usuario?.token) {
      this.consultarHabitosSistemaWeb();
    }
  }

  async consultarHabitosSistemaWeb() {
    const loading = await this.controle_carregamento.create({ message: 'Pesquisando...', duration: 60000 });
    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${API_BASE_URL}/api/habitos/`
    };

    CapacitorHttp.get(options)
      .then(async (resposta: HttpResponse) => {
        if (resposta.status == 200) {
          this.lista_habitos = resposta.data.map((habito: any) => 
            new Habito(
              habito.id,
              habito.nome,
              habito.descricao,
              habito.data || null, // Assuming `data` can be null
              habito.feito || false // Assuming `feito` defaults to false
            )
          );
          loading.dismiss();
        } else {
          loading.dismiss();
          this.apresenta_mensagem(`Falha ao consultar hábitos: código ${resposta.status}`);
        }
      })
      .catch(async (erro: any) => {
        console.log(erro);
        loading.dismiss();
        this.apresenta_mensagem(`Falha ao consultar hábitos: código ${erro?.status}`);
      });
  }

  async apresenta_mensagem(texto: string) {
    const mensagem = await this.controle_toast.create({
      message: texto,
      cssClass: 'ion-text-center',
      duration: 2000
    });
    mensagem.present();
  }

  async marcarHabito(id: number, feito: boolean) {
    const habitoParaAtualizar = this.lista_habitos.find(h => h.id === id);
    const estadoOriginal = habitoParaAtualizar ? habitoParaAtualizar.feito : null;

    if (habitoParaAtualizar) {
      habitoParaAtualizar.feito = feito;
    }

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${API_BASE_URL}/api/habitos/${id}/marcar/`,
      data: { feito }
    };

    CapacitorHttp.post(options)
      .then(async (resposta: HttpResponse) => {
        if (resposta.status === 200) {
          this.consultarHabitosSistemaWeb();
        } else {
          console.error(`Erro ao marcar hábito: ${resposta.status}`);
          if (habitoParaAtualizar && estadoOriginal !== null) {
            habitoParaAtualizar.feito = estadoOriginal;
          }
        }
      })
      .catch((erro) => {
        console.error(`Erro ao marcar hábito: ${erro}`);
        if (habitoParaAtualizar && estadoOriginal !== null) {
          habitoParaAtualizar.feito = estadoOriginal;
        }
      });
  }

  async excluirHabito(id: number) {
    const loading = await this.controle_carregamento.create({ message: 'Excluindo...', duration: 30000 });
    await loading.present();

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${API_BASE_URL}/api/habitos/${id}/deletar/`
    };

    CapacitorHttp.delete(options)
      .then(async (resposta: HttpResponse) => {
        if (resposta.status === 200 || resposta.status === 204) {
          loading.dismiss();
          this.consultarHabitosSistemaWeb();
          this.apresenta_mensagem('Hábito excluído com sucesso!');
        } else {
          loading.dismiss();
          this.apresenta_mensagem(`Falha ao excluir hábito: código ${resposta.status}`);
        }
      })
      .catch(async (erro: any) => {
        console.error('Erro ao excluir hábito:', erro);
        loading.dismiss();
        this.apresenta_mensagem(`Falha ao excluir hábito: código ${erro?.status}`);
      });
  }

  criarHabito() {
    this.exibirFormulario = true;
  }

  adicionarHabito() {
    if (this.habitoForm.invalid) {
      this.apresenta_mensagem('Preencha todos os campos!');
      return;
    }

    const novoHabito = this.habitoForm.value;

    const options: HttpOptions = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${this.usuario.token}`
      },
      url: `${API_BASE_URL}/api/habitos/criar/`,
      data: novoHabito
    };

    CapacitorHttp.post(options)
      .then(async (resposta: HttpResponse) => {
        console.log('Resposta do backend:', resposta.data);

        if (resposta.status === 201) {
          const habitoCriado = new Habito(
            resposta.data.id,
            resposta.data.nome,
            resposta.data.descricao,
            resposta.data.data || null, // Assuming `data` can be null
            resposta.data.feito || false // Assuming `feito` defaults to false
          );

          this.lista_habitos.push(habitoCriado);
          this.exibirFormulario = false;
          this.habitoForm.reset();
          this.apresenta_mensagem('Hábito adicionado com sucesso!');
        } else {
          this.apresenta_mensagem(`Erro ao adicionar hábito: ${resposta.status}`);
        }
      })
      .catch((erro) => {
        console.error('Erro ao adicionar hábito:', erro);
        this.apresenta_mensagem('Erro ao adicionar hábito!');
      });
  }

  cancelarCriacao() {
    this.exibirFormulario = false;
    this.habitoForm.reset();
  }

  async confirmarSaida() {
    const alerta = await this.alertController.create({
      header: 'Confirmação',
      message: 'Tem certeza de que deseja sair?',
      buttons: [
        {
          text: 'Cancelar',
          role: 'cancel',
          cssClass: 'secondary'
        },
        {
          text: 'Sair',
          handler: () => {
            this.sair();
          }
        }
      ]
    });

    await alerta.present();
  }

  sair() {
    this.storage.clear();
    this.controle_navegacao.navigateRoot('/home');
  }

  editarHabito(id: number) {
    this.router.navigate([`/editar-habito/${id}`]);
  }

  alternarFeito(habito: Habito) {
    const novoStatus = !habito.feito;
    this.marcarHabito(habito.id, novoStatus); // Atualiza o backend
  }
}