<template>
  <Bubble
    :options="chartOptions"
    :data="clusterInfo"
    :chart-id="chartId"
    :dataset-id-key="datasetIdKey"
    :plugins="plugins"
    :css-classes="cssClasses"
    :styles="styles"
    :width="width"
    :height="height"
    :key="chartReloadKey"
  />
</template>

<script>
import { Bubble } from "vue-chartjs";

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  PointElement,
  LinearScale,
} from "chart.js";

ChartJS.register(Title, Tooltip, Legend, PointElement, LinearScale);

export default {
  name: "BubbleChart",
  components: {
    Bubble,
  },
  props: {
    chartId: {
      type: String,
      default: "bubble-chart",
    },
    datasetIdKey: {
      type: String,
      default: "label",
    },
    width: {
      type: Number,
      default: 400,
    },
    height: {
      type: Number,
      default: 400,
    },
    cssClasses: {
      default: "",
      type: String,
    },
    styles: {
      type: Object,
      default: () => {},
    },
    plugins: {
      type: Array,
      default: () => [],
    },
  },
  data() {
    return {
      chartReloadKey: 0,
      chartData: {
        datasets: [
          {
            label: "Data One",
            backgroundColor: "#f87979",
            data: [
              {
                x: 20,
                y: 25,
                r: 5,
              },
              {
                x: 40,
                y: 10,
                r: 10,
              },
              {
                x: 30,
                y: 22,
                r: 30,
              },
            ],
          },
          {
            label: "Data Two",
            backgroundColor: "#7C8CF8",
            data: [
              {
                x: 10,
                y: 30,
                r: 15,
              },
              {
                x: 20,
                y: 20,
                r: 10,
              },
              {
                x: 15,
                y: 8,
                r: 30,
              },
            ],
          },
        ],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            ticks: {
              color: "white", // x 축의 텍스트 색상을 여기서 변경할 수 있습니다.
              min: 0, // Set the minimum value for the x-axis
              max: 3, // Set the maximum value for the x-axis
              stepSize: 1, // Set the step size to 1 to display only integer values
            },
            title: {
              display: true,
              text: "Cluster", // X 축 레이블 텍스트 설정
              color: "white",
              size: 10,
            },
          },
          y: {
            ticks: {
              color: "white", // x 축의 텍스트 색상을 여기서 변경할 수 있습니다.
              suggestedMin: 0, // Set the minimum value for the y-axis
              max: 20, // Set the maximum value for the y-axis
              step: 4, // Set the step size to 4 to display only integer values
            },
            title: {
              display: true,
              text: "평당 월세(만원)", // Y 축 레이블 텍스트 설정
              color: "white",
              size: 10,
            },
          },
        },
      },
    };
  },
  watch: {
    clusterInfo(newValue) {
      this.clusterData = newValue; // 클러스터 데이터 업데이트
      this.chartReloadKey += 1; // 차트 리로딩을 위한 키 값 증가
    },
  },
  computed: {
    clusterInfo() {
      const others = this.$store.getters.getMyOnerooms(false);
      if (others.length === 0) {
        return []; // others 배열이 비어있으면 빈 배열 반환
      }

      const newArray = others.map((item) => {
        const deposit = item.deposit;
        const rent = item.rent;
        const manage_cost = item.manage_cost;
        const area_p = item.area_p;
        const cluster = item.cluster;

        const costperRaw =
          ((deposit * 0.07 * 1.05) / 12 + rent + manage_cost) / area_p;

        const costper = parseFloat(costperRaw.toFixed(2));

        // 기존 객체의 속성을 복사하여 새로운 객체를 만듭니다.
        const newItem = {
          cluster: cluster,
          costper: costper,
        };

        return newItem;
      });
      // cluster 별로 그룹화하여 평균과 개수 계산
      const resultArray = [];
      for (let i = 0; i < 4; i++) {
        // cluster가 0부터 9까지의 정수라고 가정
        const filteredItems = newArray.filter((item) => item.cluster === i);
        const totalCount = filteredItems.length;
        const totalCostper = filteredItems.reduce(
          (acc, val) => acc + val.costper,
          0
        );
        const averageCostper = totalCostper / totalCount || 0;

        resultArray.push({
          x: i,
          y: averageCostper,
          r: totalCount,
        });
      }

      // r 값을 로그 스케일로 변환
      const logScaledData = resultArray.map((item) => ({
        x: item.x,
        y: item.y,
        r: Math.sqrt(item.r) + 20, // 로그 스케일로 변환
      }));

      const result_final = {
        datasets: [
          {
            label: "Cluster INFO",
            backgroundColor: "#f87979",
            data: logScaledData,
            pointRadius: 5, // 포인트 반지름 설정
            pointHoverRadius: 7, // 호버시 포인트 반지름 설정
            pointBorderWidth: 2, // 포인트 테두리 두께 설정
            pointBorderColor: "#fff", // 포인트 테두리 색상 설정
            pointBackgroundColor: "rgba(248, 121, 121, 0.8)", // 포인트 배경 색상 설정
          },
        ],
      };

      return result_final;
    },
  },
};
</script>
