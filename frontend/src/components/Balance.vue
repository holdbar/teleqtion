<template>
  <div v-loading="loading">
    <el-alert v-if="this.balance <= 0"
              type="warning"
              center
              description="Please, refill your balance in order to use the system.">
      <span slot="title">Your current balance is {{this.balance}} $</span>
    </el-alert>
    <h3>Top Up Balance</h3>
    <el-form :model="balanceForm"
             :inline="true"
             :rules="rules"
             :hide-required-asterisk=true
             ref="balanceForm">
      <el-form-item label="Amount" prop="amount">
        <el-input-number v-model="balanceForm.amount"
                         :precision="2"
                         :step="0.5"
                         :min="5"
                         :max="1000000">
        </el-input-number>
        <el-tag type="info">$</el-tag>
      </el-form-item>
      <el-form-item label="Currency" prop="selectedCurrency">
        <el-select v-model="balanceForm.selectedCurrency" placeholder="Select">
          <el-option
            v-for="currency in currencies"
            :key="currency.symbol"
            :label="currency.name"
            :value="currency.symbol">
            <span style="float: left">{{ currency.name }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px">{{ currency.price }} $</span>
          </el-option>
        </el-select>
        <div v-show="balanceForm.selectedCurrency && balanceForm.amount > 0">
          You will need to pay ~ {{ approximateAmount() }} {{ balanceForm.selectedCurrency }}
        </div>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onSubmit">
          Go <i class="el-icon-d-arrow-right"></i>
        </el-button>
      </el-form-item>
    </el-form>
    <el-dialog
      title="Details"
      :visible.sync="transactionDialogVisible"
      center>
      <div class="text-center">
        <p>
          Send {{this.txAmount}} {{this.txCurrency}} to
          {{this.txAddress}} to refill your balance.
        </p>
        <p>Address:
          <el-tag>{{this.txAddress}}</el-tag>
        </p>
        <p>Amount:
          <el-tag>{{this.txAmount}} {{this.txCurrency}}</el-tag>
        </p>
        <img :src="this.txQrCodeUrl" alt="transaction address qr code"/>

        <p><a :href="this.txStatusUrl" target="_blank">Transaction Status</a></p>

        <p>
          Time Left <i class="el-icon-time"></i>: {{this.countdown}}
        </p>
      </div>
    </el-dialog>


    <h4>Previous Payments</h4>
    <TransactionsTable/>
  </div>
</template>


<script>
  import {HTTP} from '../http-common';
  import TransactionsTable from './TransactionsTable'

  export default {
    components: {
      TransactionsTable
    },
    data() {
      return {
        loading: false,
        transactionDialogVisible: false,
        balance: 0,
        balanceForm: {
          amount: 5,
          selectedCurrency: '',
        },
        currencies: [],
        rules: {
          amount: [
            {required: true, message: 'Please input amount', trigger: 'blur'},
          ],
          selectedCurrency: [
            {required: true, message: 'Please select currency', trigger: 'blur'}
          ],
        },

        txAddress: '',
        txAmount: '',
        txQrCodeUrl: '',
        txStatusUrl: '',
        txTimeout: '',
        txCurrency: '',
        countdownInterval: null,
        countdown: '',
      }
    },
    methods: {
      onSubmit() {
        this.$refs['balanceForm'].validate((valid) => {
          if (valid) {
            this.createTx();
            this.txCurrency = this.balanceForm.selectedCurrency;
            this.$refs['balanceForm'].resetFields();
          } else {
            return false;
          }
        });
      },

      createTx() {
        this.loading = true;

        HTTP.post('payments/crypto/create', {
          amount: this.balanceForm.amount,
          currency: this.balanceForm.selectedCurrency
        }).then(response => {
          if (response.status === 200) {
            this.transactionDialogVisible = true;
            this.txAddress = response.data['address'];
            this.txAmount = parseFloat(response.data.amount).toFixed(8);
            this.txQrCodeUrl = response.data.qrcode_url;
            this.txStatusUrl = response.data.status_url;
            this.txTimeout = response.data.timeout;
            this.countdownInterval = setInterval(function () {
              this.countdown = this.timeLeft();
            }.bind(this), 1000);
            this.$root.$emit('updateTransactionsTable');
          } else {
            this.$notify({
              title: 'Error',
              message: 'Error accepting payment. Please, try again later.',
              type: 'error'
            });
          }
        }).catch(e => {
          this.$notify({
            title: 'Error',
            message: 'Error accepting payment. Please, try again later.',
            type: 'error'
          });
        });

        this.loading = false;
      }
      ,
      fetchBalance() {
        this.loading = true;

        HTTP.get('auth/user/')
          .then(response => {
            if (response.status === 200) {
              this.balance = response.data.balance;
            } else {
              this.$notify({
                title: 'Error',
                message: 'Error getting balance.',
                type: 'error'
              });
            }
          }).catch(e => {
          this.$notify({
            title: 'Error',
            message: 'Error getting balance.',
            type: 'error'
          });
        });

        this.loading = false;
      }
      ,
      fetchCurrencies() {
        this.loading = true;

        HTTP.get('payments/crypto/currencies')
          .then(response => {
            if (response.status === 200) {
              this.currencies = response.data;
            } else {
              this.$notify({
                title: 'Error',
                message: 'Error getting currencies.',
                type: 'error'
              });
            }
          }).catch(e => {
          this.$notify({
            title: 'Error',
            message: 'Error getting currencies.',
            type: 'error'
          });
        });
        this.loading = false;
      }
      ,
      approximateAmount() {
        let currency = this.currencies.find(
          x => x.symbol === this.balanceForm.selectedCurrency
        );
        if (currency) {
          let value = this.balanceForm.amount / currency.price;
          return value.toFixed(8);
        }
      },
      timeLeft: function () {
        let countDownDate = new Date(this.txTimeout).getTime();
        let now = new Date().getTime();
        let distance = countDownDate - now;
        let hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        let seconds = Math.floor((distance % (1000 * 60)) / 1000);
        if (distance < 0) {
          clearInterval(this.countdownInterval);
          return "EXPIRED";
        }
        return `${hours}:${minutes}:${seconds}`;
      },
    },
    mounted() {
      this.fetchBalance();
      this.fetchCurrencies();
    },
  }
</script>

<style scoped>
  .text-center {
    text-align: center;
  }
</style>
