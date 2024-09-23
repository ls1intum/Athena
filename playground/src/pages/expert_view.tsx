import SideBySideHeader from '@/components/expert_evaluation/expert_view/side_by_side_header';
import React from 'react';
import LikertScaleForm from "@/components/expert_evaluation/expert_view/likert_scale_form";

function SideBySideExpertView() {
  return (
    <div className={"bg-white p-6"}>
      <SideBySideHeader />
      <LikertScaleForm />
    </div>
  );
}

export default SideBySideExpertView;